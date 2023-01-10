# Copyright 2023 Acsone SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from odoo.tests import common

from ..models.survey_question import ODOO_TO_FORM_IO_TYPES_DICT


class TestSurveyFormIo(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey_public = cls.env["survey.survey"].create(
            {"title": "Test Public Survey", "access_mode": "public", "state": "open"}
        )
        cls.env["survey.question"].create(
            cls._get_questions_vals_list(cls, cls.survey_public.id)
        )
        cls.survey_private = cls.env["survey.survey"].create(
            {"title": "Test Private Survey", "access_mode": "token", "state": "open"}
        )
        cls.env["survey.question"].create(
            cls._get_questions_vals_list(cls, cls.survey_private.id)
        )

    def _get_questions_vals_list(self, survey_id):
        return [
            {
                "title": "Test Free Text",
                "survey_id": survey_id,
                "sequence": 1,
                "question_type": "free_text",
                "constr_mandatory": True,
            },
            {
                "title": "Test TextBox",
                "survey_id": survey_id,
                "sequence": 2,
                "question_type": "textbox",
            },
            {
                "title": "Test Numerical Box",
                "survey_id": survey_id,
                "sequence": 3,
                "question_type": "numerical_box",
                "constr_mandatory": True,
            },
            {
                "title": "Test Date",
                "survey_id": survey_id,
                "sequence": 4,
                "question_type": "date",
            },
            {
                "title": "Test Datetime",
                "survey_id": survey_id,
                "sequence": 5,
                "question_type": "datetime",
            },
            {
                "title": "Test Simple Choice",
                "survey_id": survey_id,
                "sequence": 2,
                "question_type": "simple_choice",
                "labels_ids": [
                    (0, 0, {"value": "A"}),
                    (0, 0, {"value": "B"}),
                    (0, 0, {"value": "C"}),
                ],
            },
            {
                "title": "Test Multiple choice",
                "survey_id": survey_id,
                "sequence": 2,
                "question_type": "multiple_choice",
                "labels_ids": [
                    (0, 0, {"value": 1}),
                    (0, 0, {"value": 2}),
                    (0, 0, {"value": 3}),
                ],
            },
        ]

    def _get_answers_json(self, survey_id):
        free_text_question = survey_id.question_ids.filtered(
            lambda q: q.question_type == "free_text"
        )
        text_box_question = survey_id.question_ids.filtered(
            lambda q: q.question_type == "textbox"
        )
        numerical_box_question = survey_id.question_ids.filtered(
            lambda q: q.question_type == "numerical_box"
        )
        date_question = survey_id.question_ids.filtered(
            lambda q: q.question_type == "date"
        )
        date_time_question = survey_id.question_ids.filtered(
            lambda q: q.question_type == "datetime"
        )
        simple_choice_question = survey_id.question_ids.filtered(
            lambda q: q.question_type == "simple_choice"
        )
        multiple_choice_question = survey_id.question_ids.filtered(
            lambda q: q.question_type == "multiple_choice"
        )
        return {
            "data": {
                f"q{free_text_question.id}": "test answer 1",
                f"q{text_box_question.id}": "test answer 2",
                f"q{numerical_box_question.id}": 10,
                f"q{date_question.id}": "2023-02-01T00:00:00+01:00",
                f"q{date_time_question.id}": "2023-02-01T12:00:00+01:00",
                f"q{simple_choice_question.id}": (
                    f"a{simple_choice_question.labels_ids[1].id}"
                ),
                f"q{multiple_choice_question.id}": {
                    f"a{multiple_choice_question.labels_ids[0].id}": True,
                    f"a{multiple_choice_question.labels_ids[1].id}": True,
                    f"a{multiple_choice_question.labels_ids[2].id}": False,
                },
            }
        }

    def _get_required_answers_json(self, survey_id):
        free_text_question = survey_id.question_ids.filtered(
            lambda q: q.question_type == "free_text"
        )
        return {"data": {f"q{free_text_question.id}": "test answer 1"}}

    def test_survey_formio(self):
        """
        Data:
            - Two surveys: one public and one with an access token
            - One question per question_type on those surveys
        Test case:
            - We use the generate_formio_json on both
            - Add a question of type matrix to the first survey and
              try to generate the json again.
        Expected result:
            - In both case the function should work with no error.
              Each question should be represented by the correct component
            - The json is generated without an error but the matrix question
              is ignored
        """
        public_survey_formio_dict = json.loads(
            self.survey_public.generate_formio_json()
        )
        self.assertEqual(public_survey_formio_dict["display"], "form")
        self.assertEqual(public_survey_formio_dict["title"], self.survey_public.title)
        self.assertEqual(
            len(public_survey_formio_dict["components"]),
            len(self.survey_public.question_ids) + 1,
        )  # + 1 because the title is represented as a component too
        for (i, component) in enumerate(public_survey_formio_dict["components"]):
            if i == 0:
                continue
            question = self.survey_public.question_ids[i - 1]
            self.assertEqual(
                component["type"], ODOO_TO_FORM_IO_TYPES_DICT[question.question_type]
            )
            self.assertEqual(component["key"], "q" + str(question.id))
            self.assertEqual(
                component["validate"]["required"], question.constr_mandatory
            )

        private_survey_formio_dict = json.loads(
            self.survey_private.generate_formio_json()
        )
        self.assertEqual(private_survey_formio_dict["display"], "form")
        self.assertEqual(private_survey_formio_dict["title"], self.survey_private.title)
        self.assertEqual(
            len(private_survey_formio_dict["components"]),
            len(self.survey_private.question_ids) + 1,
        )  # + 1 because the title is represented as a component too
        for (i, component) in enumerate(private_survey_formio_dict["components"]):
            if i == 0:
                continue
            question = self.survey_private.question_ids[i - 1]
            self.assertEqual(
                component["type"], ODOO_TO_FORM_IO_TYPES_DICT[question.question_type]
            )
            self.assertEqual(component["key"], "q" + str(question.id))
            self.assertEqual(component["label"], question.title)
            self.assertEqual(
                component["validate"]["required"], question.constr_mandatory
            )
            if question.question_type == "date":
                self.assertFalse(component["enableTime"])
            if question.question_type == "datetime":
                self.assertTrue(component["enableTime"])
            if question.question_type in ["simple_choice", "multiple_choice"]:
                self.assertEqual(len(component["values"]), len(question.labels_ids))
                self.assertEqual(
                    [d["label"] for d in component["values"]],
                    question.labels_ids.mapped("value"),
                )

        self.env["survey.question"].create(
            {
                "survey_id": self.survey_public.id,
                "title": "Test Matrix",
                "question_type": "matrix",
                "labels_ids": [
                    (0, 0, {"value": "A"}),
                    (0, 0, {"value": "B"}),
                    (0, 0, {"value": "C"}),
                ],
                "labels_ids_2": [
                    (0, 0, {"value": 1}),
                    (0, 0, {"value": 2}),
                    (0, 0, {"value": 3}),
                ],
            }
        )
        public_survey_formio_dict = json.loads(
            self.survey_public.generate_formio_json()
        )
        self.assertEqual(
            len(public_survey_formio_dict["components"]),
            len(self.survey_public.question_ids),
        )

    def test_to_user_input_all_questions_answered(self):
        """
        Data:
            - Two surveys: one public and one with an access token
            - A JSON representing answers to those surveys
        Test case:
            - We use the user_input_from_formio function on both surveys
              with the JSON
        Expected result:
            - In both case the function should work with no error.
              The answers should have the values given in the JSON
        """
        self.assertEqual(self.survey_public.answer_count, 0)
        answers = self._get_answers_json(self.survey_public)
        self.survey_public.user_input_from_formio(answers)
        self.assertEqual(self.survey_public.answer_count, 1)
        user_input = self.survey_public.user_input_ids[0]

        # 7 questions answered but for the multiple choice there's a line per answer
        self.assertEqual(len(user_input.user_input_line_ids), 9)
        self.assertEqual(
            user_input.user_input_line_ids.filtered(
                lambda uil: uil.answer_type == "free_text"
            ).value_free_text,
            "test answer 1",
        )
        self.assertEqual(
            user_input.user_input_line_ids.filtered(
                lambda uil: uil.answer_type == "number"
            ).value_number,
            10,
        )
        simple_choice_question = self.survey_public.question_ids.filtered(
            lambda q: q.question_type == "simple_choice"
        )
        self.assertEqual(
            user_input.user_input_line_ids.filtered(
                lambda uil: uil.question_id == simple_choice_question
            ).value_suggested,
            simple_choice_question.labels_ids[1],
        )

        self.assertEqual(self.survey_private.answer_count, 0)
        answers = self._get_answers_json(self.survey_private)
        self.survey_private.user_input_from_formio(answers)
        self.assertEqual(self.survey_private.answer_count, 1)

    def test_to_user_input_only_required_questions_answered(self):
        """
        Data:
            - Two surveys: one public and one with an access token
            - A JSON representing only the required answers to those surveys
        Test case:
            - We use the user_input_from_formio function on both surveys
              with the JSON
        Expected result:
            - In both case the function should work with no error.
              The answers should have the values given in the JSON
        """
        self.assertEqual(self.survey_public.answer_count, 0)
        answers = self._get_required_answers_json(self.survey_public)
        self.survey_public.user_input_from_formio(answers)
        self.assertEqual(self.survey_public.answer_count, 1)
        user_input = self.survey_public.user_input_ids[0]
        self.assertEqual(len(user_input.user_input_line_ids), 1)
        self.assertEqual(
            user_input.user_input_line_ids.filtered(
                lambda uil: uil.answer_type == "free_text"
            ).value_free_text,
            "test answer 1",
        )

        self.assertEqual(self.survey_private.answer_count, 0)
        answers = self._get_required_answers_json(self.survey_private)
        self.survey_private.user_input_from_formio(answers)
        self.assertEqual(self.survey_private.answer_count, 1)

    def test_to_user_input_with_user_input_id_answer(self):
        """
        Data:
            - Two surveys: one public and one with an access token
            - Two user_inputs : one for each survey
            - A JSON representing answers to those surveys
        Test case:
            - We use the user_input_from_formio function on both surveys
              with the JSON and the user_input_id
        Expected result:
            - In both case the function should work with no error.
              The answers should have the values given in the JSON
        """
        public_user_input = self.survey_public._create_answer()
        self.assertEqual(self.survey_public.answer_count, 1)
        answers = self._get_answers_json(self.survey_public)
        self.survey_public.user_input_from_formio(answers, public_user_input.id)
        self.assertEqual(self.survey_public.answer_count, 1)
        user_input = self.survey_public.user_input_ids[0]

        # 7 questions answered but for the multiple choice there's a line per answer
        self.assertEqual(len(user_input.user_input_line_ids), 9)
        self.assertEqual(
            user_input.user_input_line_ids.filtered(
                lambda uil: uil.answer_type == "free_text"
            ).value_free_text,
            "test answer 1",
        )
        self.assertEqual(
            user_input.user_input_line_ids.filtered(
                lambda uil: uil.answer_type == "number"
            ).value_number,
            10,
        )
        simple_choice_question = self.survey_public.question_ids.filtered(
            lambda q: q.question_type == "simple_choice"
        )
        self.assertEqual(
            user_input.user_input_line_ids.filtered(
                lambda uil: uil.question_id == simple_choice_question
            ).value_suggested,
            simple_choice_question.labels_ids[1],
        )

        private_user_input = self.survey_private._create_answer()
        self.assertEqual(self.survey_private.answer_count, 1)
        answers = self._get_answers_json(self.survey_private)
        self.survey_private.user_input_from_formio(answers, private_user_input.id)
        self.assertEqual(self.survey_private.answer_count, 1)
