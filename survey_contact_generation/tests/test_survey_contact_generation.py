# Copyright 2023 Tecnativa - David Vidal
# Copyright 2023 Tecnativa - Stefan Ungureanu
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import HttpCase, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class SurveyContactGenerationCase(SurveyCase, HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.survey = self.env.ref("survey_contact_generation.survey_contact_creation")
        initial_user_inputs = self.survey.user_input_ids
        # Run the survey as a portal user and get the generated quotation
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_contact_generation",
            step_delay=1000,
        )
        self.user_input = self.survey.user_input_ids - initial_user_inputs


@tagged("-at_install", "post_install")
class SurveyContactGenerationTests(SurveyContactGenerationCase):
    def test_contact_generation(self):
        partner = self.env["res.partner"].search(
            [("email", "=", "survey_contact_generation@test.com")]
        )
        self.assertEqual(partner, self.user_input.partner_id)
        self.assertEqual(partner.parent_id.name, "My Company Name")
        self.assertEqual(partner.generating_survey_user_input_id, self.user_input)
