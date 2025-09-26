# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError

from odoo.addons.survey.tests import common


class TestSurvey(common.SurveyCase):
    def setUp(self):
        super().setUp()
        User = self.env["res.users"].with_context(**{"no_reset_password": True})
        (group_survey_user, group_employee) = (
            self.ref("survey.group_survey_user"),
            self.ref("base.group_user"),
        )
        self.survey_manager = User.create(
            {
                "name": "Maria Riera",
                "login": "Riera",
                "email": "maria.riera@example.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.ref("survey.group_survey_manager"),
                            group_survey_user,
                            group_employee,
                        ],
                    )
                ],
            }
        )
        self.survey1 = (
            self.env["survey.survey"]
            .with_user(self.survey_manager)
            .create({"title": "S0", "page_ids": [(0, 0, {"title": "P0"})]})
        )
        self.page1 = (
            self.env["survey.question"]
            .with_user(self.survey_manager)
            .create(
                {
                    "title": "First page",
                    "survey_id": self.survey1.id,
                    "sequence": 1,
                    "is_page": True,
                }
            )
        )
        self.user_input1 = (
            self.env["survey.user_input"]
            .with_user(self.survey_manager)
            .create(
                {
                    "survey_id": self.survey1.id,
                    "partner_id": self.survey_manager.partner_id.id,
                }
            )
        )
        self.question1 = (
            self.env["survey.question"]
            .with_user(self.survey_manager)
            .create(
                {
                    "title": "Test NPS Rate",
                    "page_id": self.page1.id,
                    "question_type": "nps_rate",
                    "validation_required": True,
                }
            )
        )
        self.question2 = (
            self.env["survey.question"]
            .with_user(self.survey_manager)
            .create(
                {
                    "page_id": self.page1.id,
                    "question_type": "numerical_box",
                    "title": "Question 2",
                }
            )
        )

    def test_01_question_nps_rate_with_error_values(self):
        error_results = [
            ("aaa", "This is not a number"),
            ("-1", "Answer is not in the right range"),
            ("11", "Answer is not in the right range"),
        ]
        for i in range(len(error_results)):
            self.assertEqual(
                self.question1.validate_question(error_results[i][0]),
                {self.question1.id: error_results[i][1]},
            )
        self.question1.validation_required = False
        self.assertEqual(
            self.question1.validate_question(-1),
            {},
        )

    def test_02_question_nps_rate_with_valid_values(self):
        for i in ("0", "6", "8"):
            self.user_input1._save_lines(question=self.question1, answer=i)
            self.assertEqual(
                self.user_input1.user_input_line_ids.filtered(
                    lambda r: r.question_id == self.question1
                ).value_numerical_box,
                float(i),
            )
            self.assertEqual(self.question1.validate_question(i), {})
        self.assertTrue(
            self.question1._get_stats_summary_data(
                self.user_input1.user_input_line_ids.filtered(
                    lambda r: r.question_id == self.question1
                )
            )
        )

    def test_03_question_nps_rate_with_constr_mandatory(self):
        self.question1.constr_mandatory = True
        with self.assertRaises(ValidationError):
            self.user_input1._save_lines(question=self.question1, answer="0")
        with self.assertRaises(ValidationError):
            self.user_input1._save_lines(question=self.question1, answer="11")

    def test_04_question_nps_rate_validation_errors(self):
        with self.assertRaises(ValidationError):
            self.user_input1._save_lines(question=self.question1, answer="-1")
        survey_user_input_line_obj = self.env["survey.user_input.line"]
        with self.assertRaises(ValidationError):
            input_line_1 = survey_user_input_line_obj.create(
                [
                    {
                        "user_input_id": self.user_input1.id,
                        "question_id": self.question1.id,
                        "value_char_box": "Lukas",
                    }
                ]
            )
            input_line_1.answer_type = False
        with self.assertRaises(ValidationError):
            survey_user_input_line_obj.create(
                [
                    {
                        "user_input_id": self.user_input1.id,
                        "question_id": self.question1.id,
                        "answer_type": "char_box",
                        "value_char_box": "lukas",
                    }
                ]
            )

    def test_05_other_questions(self):
        self.user_input1._save_lines(question=self.question2, answer="2")
        self.assertEqual(self.question2.validate_question("2"), {})
        self.assertTrue(
            self.question2._get_stats_summary_data(
                self.user_input1.user_input_line_ids.filtered(
                    lambda r: r.question_id == self.question2
                )
            )
        )
