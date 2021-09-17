# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import random

from odoo.exceptions import ValidationError

from odoo.addons.survey.tests import common


class TestSurvey(common.SurveyCase):
    def setUp(self):
        super(TestSurvey, self).setUp()
        User = self.env["res.users"].with_context({"no_reset_password": True})
        (group_survey_user, group_employee) = (
            self.ref("survey.group_survey_user"),
            self.ref("base.group_user"),
        )
        self.survey_manager = User.create(
            {
                "name": "Nerea Riera",
                "login": "Riera",
                "email": "nerea.riera@example.com",
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
                    "title": "Test Star Rate",
                    "page_id": self.page1.id,
                    "question": "Q0",
                    "question_type": "star_rate",
                    "validation_required": True,
                }
            )
        )
        self.answer_tag1 = "{}_{}_{}".format(
            self.survey1.id,
            self.page1.id,
            self.question1.id,
        )
        self._type_match["star_rate"] = ("number", "value_number")

    def test_01_question_star_rate_with_error_values(self):
        error_results = [
            ("aaa", "This is not a number"),
            ("-1", "Answer is not in the right range"),
            ("6", "Answer is not in the right range"),
        ]
        msg = (
            "Validation function for type numerical_box is unable to "
            "notify if answer is violating the validation rules"
        )
        for i in range(len(error_results)):
            self.assertEqual(
                self.question1.validate_question(
                    {self.answer_tag1: error_results[i][0]}, self.answer_tag1
                ),
                {self.answer_tag1: error_results[i][1]},
                msg=msg,
            )

    def test_02_question_star_rate_with_valid_values(self):
        for i in ("0", "3", "5"):
            self.assertTrue(
                self.env["survey.user_input_line"].save_line_star_rate(
                    user_input_id=self.user_input1.id,
                    question=self.question1,
                    post={self.answer_tag1: i},
                    answer_tag=self.answer_tag1,
                )
            )

    def test_03_question_star_rate_with_constr_mandatory(self):
        self.question1.constr_mandatory = True
        with self.assertRaises(ValidationError):
            self.env["survey.user_input_line"].save_line_star_rate(
                user_input_id=self.user_input1.id,
                question=self.question1,
                post={self.answer_tag1: "0"},
                answer_tag=self.answer_tag1,
            )

    def test_survey(self):
        num = [float(n) for n in random.sample(range(1, 5), 3)]
        nsum = sum(num)
        for i in range(3):
            answer = self._add_answer(self.survey1, False, email="public@example.com")
            self._add_answer_line(self.question1, answer, str(num[i]))
        exresult = {
            "average": round((nsum / len(num)), 2),
            "max": round(max(num), 2),
            "min": round(min(num), 2),
            "sum": nsum,
        }
        result = self.env["survey.survey"].prepare_result(self.question1)
        for key in exresult:
            self.assertEqual(result[key], exresult[key])
