# Copyright 2025 Binhex - Adasat Torres de Leon
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.survey.tests import common


class TestSurvey(common.SurveyCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = cls.env["res.users"].with_context(no_reset_password=True)
        (group_survey_manager, group_employee) = (
            cls.env.ref("survey.group_survey_manager").id,
            cls.env.ref("base.group_user").id,
        )

        cls.manager = User.create(
            {
                "name": "Manager",
                "login": "manager",
                "email": "manager@test.com",
                "groups_id": [(6, 0, [group_survey_manager, group_employee])],
            }
        )

        cls.survey1 = (
            cls.env["survey.survey"]
            .with_user(cls.manager)
            .create(
                {
                    "title": "Survey with test",
                    "page_ids": [(0, 0, {"title": "Page0"})],
                    "users_can_go_back": False,
                }
            )
        )

        cls.page1 = (
            cls.env["survey.question"]
            .with_user(cls.manager)
            .create(
                {
                    "title": "Page1",
                    "survey_id": cls.survey1.id,
                    "sequence": 1,
                    "is_page": True,
                }
            )
        )

        cls.user_input1 = (
            cls.env["survey.user_input"]
            .with_user(cls.manager)
            .create(
                {
                    "survey_id": cls.survey1.id,
                    "partner_id": cls.manager.partner_id.id,
                }
            )
        )

        cls.question_test = (
            cls.env["survey.question"]
            .with_user(cls.manager)
            .create(
                {
                    "title": "Signature",
                    "survey_id": cls.survey1.id,
                    "page_id": cls.page1.id,
                    "question_type": "char_box",
                    "sequence": 2,
                    "constr_mandatory": True,
                    "constr_error_msg": "Error",
                }
            )
        )

    def test01_validate_question(self):
        self.assertEqual(
            self.question_test.validate_question(answer=False),
            {self.question_test.id: self.question_test.constr_error_msg},
        )
        self.survey1.write({"users_can_go_back": True})
        self.assertEqual(
            self.question_test.validate_question(answer=False),
            {},
        )
