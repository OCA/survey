# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSurvey(TransactionCase):
    def setUp(self):
        super().setUp()
        self.survey = self.env["survey.survey"].create({"title": "Test Survey"})
        self.question_multiple_choice = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "question_type": "multiple_choice",
                "title": "Which Hogwarts houses do you like?",
            }
        )
        # Create suggested answers
        self.gryffindor = self.env["survey.question.answer"].create(
            {
                "question_id": self.question_multiple_choice.id,
                "value": "Gryffindor",
            }
        )
        self.ravenclaw = self.env["survey.question.answer"].create(
            {
                "question_id": self.question_multiple_choice.id,
                "value": "Ravenclaw",
            }
        )
        self.hufflepuff = self.env["survey.question.answer"].create(
            {
                "question_id": self.question_multiple_choice.id,
                "value": "Hufflepuff",
            }
        )
        self.slytherin = self.env["survey.question.answer"].create(
            {
                "question_id": self.question_multiple_choice.id,
                "value": "Slytherin",
            }
        )

        # Different answers
        self.zero_answers = []
        self.one_answer = [self.gryffindor.id]
        self.three_answers = [self.gryffindor, self.slytherin, self.hufflepuff]
        self.four_answers = [
            self.gryffindor,
            self.slytherin,
            self.hufflepuff,
            self.ravenclaw,
        ]

    def test_multiple_choice_no_limitation(self):
        """
        Multiple choice question without number of answers limitation
        """
        self.assertEqual(
            {}, self.question_multiple_choice.validate_question(self.zero_answers)
        )
        self.assertEqual(
            {}, self.question_multiple_choice.validate_question(self.one_answer)
        )
        self.assertEqual(
            {}, self.question_multiple_choice.validate_question(self.three_answers)
        )
        self.assertEqual(
            {}, self.question_multiple_choice.validate_question(self.four_answers)
        )

    def test_multiple_choice_limitation_0_3(self):
        """
        Multiple choice question with max 3 allowed answers.
        """
        error_msg = "TOO MANY ANSWERS"
        self.question_multiple_choice.write(
            {
                "validation_required": True,
                "validation_multiple_answers_max": 3,
                "validation_error_msg": error_msg,
            }
        )
        self.assertEqual(
            {}, self.question_multiple_choice.validate_question(self.zero_answers)
        )
        self.assertEqual(
            {}, self.question_multiple_choice.validate_question(self.one_answer)
        )
        self.assertEqual(
            {}, self.question_multiple_choice.validate_question(self.three_answers)
        )
        self.assertEqual(
            {self.question_multiple_choice.id: error_msg},
            self.question_multiple_choice.validate_question(self.four_answers),
        )

    def test_multiple_choice_limitation_1_3(self):
        """
        Multiple choice question with min 1 and max 3 allowed answers.
        """
        error_msg = "TOO MANY ANSWERS"
        self.question_multiple_choice.write(
            {
                "validation_required": True,
                "validation_multiple_answers_min": 1,
                "validation_multiple_answers_max": 3,
                "validation_error_msg": error_msg,
            }
        )
        self.assertEqual(
            {self.question_multiple_choice.id: error_msg},
            self.question_multiple_choice.validate_question(self.zero_answers),
        )
        self.assertEqual(
            {}, self.question_multiple_choice.validate_question(self.one_answer)
        )
        self.assertEqual(
            {}, self.question_multiple_choice.validate_question(self.three_answers)
        )
        self.assertEqual(
            {self.question_multiple_choice.id: error_msg},
            self.question_multiple_choice.validate_question(self.four_answers),
        )

    def test_multiple_choice_limitation_3_3(self):
        """
        Multiple choice question with exactly 3 allowed answers.
        """
        error_msg = "TOO MANY ANSWERS"
        self.question_multiple_choice.write(
            {
                "validation_required": True,
                "validation_multiple_answers_min": 3,
                "validation_multiple_answers_max": 3,
                "validation_error_msg": error_msg,
            }
        )
        self.assertEqual(
            {self.question_multiple_choice.id: error_msg},
            self.question_multiple_choice.validate_question(self.zero_answers),
        )
        self.assertEqual(
            {self.question_multiple_choice.id: error_msg},
            self.question_multiple_choice.validate_question(self.one_answer),
        )
        self.assertEqual(
            {}, self.question_multiple_choice.validate_question(self.three_answers)
        )
        self.assertEqual(
            {self.question_multiple_choice.id: error_msg},
            self.question_multiple_choice.validate_question(self.four_answers),
        )

    def test_multiple_choice_limitation_0_0(self):
        """
        If a user activates the validation_required (for another reason
        than limiting the number of allowed answers) but keeps
        validation_multiple_answers_max to 0, the check must not be applied.
        -> Answering with 3 answers is allowed.
        """
        error_msg = "TOO MANY ANSWERS"
        self.question_multiple_choice.write(
            {
                "validation_required": True,
                "validation_multiple_answers_min": 0,
                "validation_multiple_answers_max": 0,
                "validation_error_msg": error_msg,
            }
        )
        self.assertEqual(
            {},
            self.question_multiple_choice.validate_question(self.three_answers),
        )
