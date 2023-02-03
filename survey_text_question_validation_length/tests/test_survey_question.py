# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSurvey(TransactionCase):
    def setUp(self):
        super().setUp()
        self.survey = self.env["survey.survey"].create({"title": "Test Survey"})
        self.answer_size_0 = ""
        self.answer_size_5 = "ABCDE"
        self.answer_size_10 = "ABCDEFGHIJ"
        self.answer_size_15 = "ABCDEFGHIJKLMNO"

    def test_text_box_no_limitation(self):
        """
        Text box question without length limitation.
        """
        question = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "question_type": "text_box",
                "title": "Text box question without length limitation",
            }
        )
        self.assertEqual({}, question.validate_question(self.answer_size_0))
        self.assertEqual({}, question.validate_question(self.answer_size_5))
        self.assertEqual({}, question.validate_question(self.answer_size_10))
        self.assertEqual({}, question.validate_question(self.answer_size_15))

    def test_text_box_limitation_0_10(self):
        """
        Text box question with length limitation (0-10 characters).
        """
        error_msg = "TOO LONG"
        question = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "question_type": "text_box",
                "title": "Text box question with length limitation 0-10",
                "validation_required": True,
                "validation_length_max": 10,
                "validation_error_msg": error_msg,
            }
        )
        self.assertEqual({}, question.validate_question(self.answer_size_0))
        self.assertEqual({}, question.validate_question(self.answer_size_5))
        self.assertEqual({}, question.validate_question(self.answer_size_10))
        self.assertEqual(
            {question.id: error_msg}, question.validate_question(self.answer_size_15)
        )

    def test_text_box_limitation_7_13(self):
        """
        Text box question with length limitation (7-13 characters).
        """
        error_msg = "TOO LONG OR TOO SHORT"
        question = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "question_type": "text_box",
                "title": "Text box question with length limitation 7-13",
                "validation_required": True,
                "validation_length_min": 7,
                "validation_length_max": 13,
                "validation_error_msg": error_msg,
            }
        )
        self.assertEqual(
            {question.id: error_msg}, question.validate_question(self.answer_size_0)
        )
        self.assertEqual(
            {question.id: error_msg}, question.validate_question(self.answer_size_5)
        )
        self.assertEqual({}, question.validate_question(self.answer_size_10))
        self.assertEqual(
            {question.id: error_msg}, question.validate_question(self.answer_size_15)
        )
