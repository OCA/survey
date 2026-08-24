# Copyright 2026 Tecnativa - Eduardo Ezerouali
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class TestContactGenerationModelSelection(SurveyCase, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = cls.env["survey.survey"].create(
            {
                "title": "Test Question Model",
                "questions_layout": "one_page",
                "access_mode": "public",
                "users_can_go_back": True,
                "generate_contact": True,
            }
        )
        cls.question1 = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Name",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__name").id,
            }
        )
        cls.question2 = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Email",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__email").id,
            }
        )
        cls.question3 = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "State",
                "question_type": "model",
                "question_model_id": cls.env.ref("base.model_res_country_state").id,
                "question_domain": '[("country_id", "in", [{}])]'.format(
                    cls.env.ref("base.es").id
                ),
            }
        )
        cls.initial_user_inputs = cls.survey.user_input_ids

    def test_question_model(self):
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_tour_contact_generation_model_selection",
        )
        user_input = self.survey.user_input_ids - self.initial_user_inputs
        partner = self.env["res.partner"].search(
            [("email", "=", "survey_contact_generation@test.com")]
        )
        self.assertEqual(partner, user_input.partner_id)
