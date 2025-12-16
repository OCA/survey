# Copyright 2026 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("-at_install", "post_install")
class TestContactGenerationModelSelection(BaseCommon, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = cls.env["survey.survey"].create(
            {
                "title": "Test Question Model",
                "survey_type": "custom",
                "questions_layout": "one_page",
                "access_mode": "public",
                "access_token": "b137640d-14d4-4748-9ef6-344caaaaaaf",
                "generate_contact": True,
            }
        )
        cls.question = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Name",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__name").id,
            }
        )
        cls.question = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Email",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__email").id,
            }
        )
        cls.question = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "State",
                "question_type": "model",
                "question_model_id": 81,
                "question_domain": '[("country_id", "in", [68])]',
            }
        )
        cls.initial_user_inputs = cls.survey.user_input_ids

    def test_question_model(self):
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_question_model",
        )
        user_input = self.survey.user_input_ids - self.initial_user_inputs
        partner = self.env["res.partner"].search(
            [("email", "=", "survey_contact_generation@test.com")]
        )
        self.assertEqual(partner, user_input.partner_id)
