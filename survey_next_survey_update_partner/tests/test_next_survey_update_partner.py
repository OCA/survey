# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import HttpCase, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class SurveyContactGenerationCase(SurveyCase, HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.origin_survey = self.env.ref(
            "survey_contact_generation.survey_contact_creation"
        )
        self.next_survey = self.env.ref(
            "survey_next_survey_update_partner.survey_next_contact"
        )
        self.existing_inputs = self.origin_survey.user_input_ids
        # Let's links several questions
        self.origin_survey.next_survey_id = self.next_survey
        self.env.ref(
            "survey_contact_generation.survey_contact_q0"
        ).next_survey_question_id = self.env.ref(
            "survey_next_survey_update_partner.survey_next_contact_q0"
        )
        self.env.ref(
            "survey_contact_generation.survey_contact_q_company_name"
        ).next_survey_question_id = self.env.ref(
            "survey_next_survey_update_partner.survey_next_contact_q_company_name"
        )

    def test_contact_generation(self):
        # Generate the contact first
        self.start_tour(
            f"/survey/start/{self.origin_survey.access_token}",
            "test_survey_contact_generation",
        )
        new_input = self.origin_survey.user_input_ids - self.existing_inputs
        partner = self.env["res.partner"].search(
            [("email", "=", "survey_contact_generation@test.com")]
        )
        self.assertEqual(partner.name, "My Name")
        self.assertEqual(partner.parent_id.name, "My Company Name")
        next_answer = new_input.next_survey_input_id
        self.start_tour(
            f"/survey/{self.next_survey.access_token}/{next_answer.access_token}",
            "test_survey_contact_update",
        )
        self.assertEqual(partner.name, "My Updated Name")
        self.assertEqual(partner.parent_id.name, "My Updated Company Name")
        self.assertEqual(partner.street, "Main Street, 42")
