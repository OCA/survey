from odoo.addons.survey.tests.common import SurveyCase


class TestSurveyUserInput(SurveyCase):
    def setUp(self):
        super().setUp()
        self.survey = self.env["survey.survey"].create(
            {"title": "Test Survey", "generate_contact": True}
        )
        self.name_question = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "title": "Name Question",
                "question_type": "char_box",
                "res_partner_field": self.env["ir.model.fields"]
                .search([("model", "=", "res.partner"), ("name", "=", "name")])
                .id,
            }
        )
        self.comment_question = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "title": "Comment Question",
                "question_type": "char_box",
                "res_partner_field": self.env["ir.model.fields"]
                .search([("model", "=", "res.partner"), ("name", "=", "comment")])
                .id,
            }
        )
        self.email_question = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "title": "Email Question",
                "question_type": "char_box",
                "res_partner_field": self.env["ir.model.fields"]
                .search([("model", "=", "res.partner"), ("name", "=", "email")])
                .id,
            }
        )
        self.user_input = self.env["survey.user_input"].create(
            {"survey_id": self.survey.id}
        )
        self.name_user_input_answer = self.env["survey.user_input.line"].create(
            {
                "user_input_id": self.user_input.id,
                "question_id": self.name_question.id,
                "value_char_box": "Partner 01",
                "answer_type": "char_box",
            }
        )
        self.comment_user_input_answer = self.env["survey.user_input.line"].create(
            {
                "user_input_id": self.user_input.id,
                "question_id": self.comment_question.id,
                "value_char_box": "Comment Partner 01",
                "answer_type": "char_box",
            }
        )
        self.email_user_input_answer = self.env["survey.user_input.line"].create(
            {
                "user_input_id": self.user_input.id,
                "question_id": self.email_question.id,
                "value_char_box": "partner01@example.com",
                "answer_type": "char_box",
            }
        )

    def test_prepare_partner(self):
        prepared_vals = self.user_input._prepare_partner()
        self.assertTrue(prepared_vals)
        self.assertTrue(prepared_vals.get("name") == "Partner 01")
        self.assertTrue(prepared_vals.get("email") == "partner01@example.com")
        self.assertTrue(
            prepared_vals.get("comment") == "\nComment Question: Comment Partner 01"
        )
