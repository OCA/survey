from odoo.tests import new_test_user, tagged

from odoo.addons.survey.tests.common import TestSurveyCommon


@tagged("-at_install", "post_install", "functional")
class TestSurveyResultMail(TestSurveyCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = new_test_user(
            cls.env,
            login="test-user",
            name="test user",
            email="testuser@test.com",
            groups="survey.group_survey_user",
        )
        cls.survey = cls.env["survey.survey"].create(
            {
                "title": "Test Survey Resul Mail",
                "access_mode": "public",
                "users_login_required": True,
                "send_result_mail": True,
            }
        )

    def test_certification_auto_sending(self):
        q_01 = self._add_question(
            page=False,
            name="2+2",
            qtype="simple_choice",
            sequence=1,
            constr_mandatory=True,
            constr_error_msg="Please select an answer",
            survey_id=self.survey.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4"},
                {"value": "5"},
            ],
        )
        q_02 = self._add_question(
            page=False,
            name="2x2",
            qtype="simple_choice",
            sequence=2,
            constr_mandatory=True,
            constr_error_msg="Please select an answer",
            survey_id=self.survey.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4"},
                {"value": "5"},
            ],
        )
        answer = self._add_answer(self.survey, self.user.partner_id)
        self._add_answer_line(q_01, answer, q_01.suggested_answer_ids[2].id)
        self._add_answer_line(q_02, answer, q_02.suggested_answer_ids[2].id)
        answer.with_user(self.user).write({"state": "done"})
        answer._mark_done()
        # Verify that the result has been sent automatically.
        mail = self.env["mail.message"].search(
            [
                ("res_id", "=", answer.id),
                ("model", "=", "survey.user_input"),
                ("subject", "ilike", "Results for"),
            ]
        )
        self.assertTrue(mail)
