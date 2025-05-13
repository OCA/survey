# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from markupsafe import Markup

from odoo.tests import HttpCase, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class SurveyCrmGenerationCase(SurveyCase, HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.oca_leads = self.env.ref("survey_crm_generation.oca_partnership_leads")
        self.survey = self.env.ref("survey_crm_generation.become_partner")
        initial_user_inputs = self.survey.user_input_ids
        # Run the survey as a portal user and get the generated quotation
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_crm_generation",
            login="portal",
        )
        self.user_input = self.survey.user_input_ids - initial_user_inputs
        self.generated_lead = self.user_input.opportunity_id


@tagged("-at_install", "post_install")
class SurveyCrmGenerationTests(SurveyCrmGenerationCase):
    def test_lead_generation(self):
        self.assertFalse(self.generated_lead.stage_id.is_won)
        self.assertEqual(self.generated_lead.team_id, self.oca_leads)
        self.assertEqual(
            self.generated_lead.tag_ids,
            (
                self.env.ref("survey_crm_generation.tag_oca_partnership")
                + self.env.ref("survey_crm_generation.tag_survey_leads")
            ),
        )
        expected_lead_description = Markup(
            "<li><em>E-mail address</em>: <b>test@test.com</b></li>"
            "<li><em>Your company name?</em>: <b>Tecnativa</b></li>"
            "<li><em>And your name?</em>: <b>Tecnativa</b></li>"
        )
        self.assertEqual(
            self.generated_lead.description,
            expected_lead_description,
        )
        self.assertEqual("Mr. Odoo", self.generated_lead.referred)
