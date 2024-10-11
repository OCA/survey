# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import HttpCase, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class SurveySaleGenerationCase(SurveyCase, HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.support_hours = self.env.ref("survey_sale_generation.support_hours")
        self.gold_service = self.env.ref("survey_sale_generation.gold_service")
        self.advanced_backup = self.env.ref("survey_sale_generation.advanced_backup")
        self.mail_management = self.env.ref("survey_sale_generation.mail_management")
        self.support_hiring_team = self.env.ref("survey_sale_generation.support_hiring")
        self.survey = self.env.ref("survey_sale_generation.survey_hire_support")
        initial_user_inputs = self.survey.user_input_ids
        # Run the survey as a portal user and get the generated quotation
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_sale_generation",
            login="portal",
        )
        self.user_input = self.survey.user_input_ids - initial_user_inputs
        self.generated_sale = self.user_input.sale_order_id


@tagged("-at_install", "post_install")
class SurveySaleGenerationTests(SurveySaleGenerationCase):
    def test_sale_generation(self):
        """Our generated sale should have these lines:

        name              price_subtotal   product_uom_qty
        --------------------------------------------------
        Gold support            $1000.00             1.000
        Advanced Backup          $500.00             1.000
        Mail Management          $500.00             1.000
        Support hours            $300.00             3.000
        """
        expected_lines = {
            self.support_hours: 3,
            self.gold_service: 3,
            self.advanced_backup: 1,
            self.mail_management: 1,
        }
        resulting_lines = {
            line.product_id: line.product_uom_qty
            for line in self.generated_sale.order_line
        }
        self.assertEqual(resulting_lines, expected_lines)
        self.assertEqual(self.generated_sale.team_id, self.support_hiring_team)
        self.assertEqual(
            self.generated_sale.partner_id, self.env.ref("base.partner_demo_portal")
        )
        info_message, *_ = self.generated_sale.message_ids
        # Some other survey inputs can be annotated in the quotation chatter
        self.assertTrue("test@test.com" in info_message.body)
        self.assertEqual("Mr. Odoo", self.generated_sale.origin)
