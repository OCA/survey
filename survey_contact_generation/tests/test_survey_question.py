from odoo.addons.survey.tests.common import SurveyCase


class TestSurveyQuestion(SurveyCase):
    def setUp(self):
        super().setUp()
        self.char_box_survey_question = self.env["survey.question"].create(
            {
                "title": "CharBox Question",
                "question_type": "char_box",
            }
        )
        self.text_box_survey_question = self.env["survey.question"].create(
            {
                "title": "TextBox Question",
                "question_type": "text_box",
            }
        )
        self.multiple_choice_survey_question = self.env["survey.question"].create(
            {
                "title": "MultipleChoice Question",
                "question_type": "multiple_choice",
            }
        )
        self.simple_choice_survey_question = self.env["survey.question"].create(
            {
                "title": "SimpleChoice Question",
                "question_type": "simple_choice",
                "res_partner_field": self.env["ir.model.fields"]
                .search([("model", "=", "res.partner"), ("name", "=", "company_id")])
                .id,
            }
        )

    def test_compute_allowed_field_ids(self):
        self.char_box_survey_question._compute_allowed_field_ids()
        char_box_allowed_field_ids = self.char_box_survey_question.allowed_field_ids.ids
        char_box_expected_field_ids = (
            self.env["ir.model.fields"]
            .search(
                [
                    ("model", "=", "res.partner"),
                    ("ttype", "in", ["char", "text"]),
                ]
            )
            .ids
        )
        self.text_box_survey_question._compute_allowed_field_ids()
        text_box_allowed_field_ids = self.text_box_survey_question.allowed_field_ids.ids
        text_box_expected_field_ids = (
            self.env["ir.model.fields"]
            .search(
                [
                    ("model", "=", "res.partner"),
                    ("ttype", "=", "html"),
                ]
            )
            .ids
        )
        self.multiple_choice_survey_question._compute_allowed_field_ids()
        multiple_choice_allowed_field_ids = (
            self.multiple_choice_survey_question.allowed_field_ids.ids
        )
        multiple_choice_expected_field_ids = (
            self.env["ir.model.fields"]
            .search(
                [
                    ("model", "=", "res.partner"),
                    ("ttype", "in", ["many2many", "html", "char"]),
                ]
            )
            .ids
        )

        self.assertEqual(char_box_allowed_field_ids, char_box_expected_field_ids)
        self.assertEqual(text_box_allowed_field_ids, text_box_expected_field_ids)
        self.assertEqual(
            multiple_choice_allowed_field_ids, multiple_choice_expected_field_ids
        )

    def test_question_answer_default_get(self):
        self.simple_choice_survey_question.with_context(
            default_res_partner_field=self.simple_choice_survey_question.res_partner_field.id
        ).write({"suggested_answer_ids": [(0, 0, {"value": "Company With Id 1"})]})
        # Question uses company_id field, therefore id=1 by default
        # since it always be at least 1 company
        self.assertEqual(
            self.simple_choice_survey_question.suggested_answer_ids.res_partner_field_resource_ref.id,  # noqa: B950
            1,
        )
