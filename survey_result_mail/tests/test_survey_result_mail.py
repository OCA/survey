from odoo.tests import tagged

from odoo.addons.survey.tests.common import TestSurveyCommon


@tagged("-at_install", "post_install", "functional")
class TestSurveyResultMail(TestSurveyCommon):
    def test_certification_auto_sending(self):
        survey = self.env["survey.survey"].create(
            {
                "title": "Test Survey Resul Mail",
                "access_mode": "public",
                "users_login_required": True,
                "send_result_mail": True,
            }
        )
        q_01 = self._add_question(
            None,
            "2+2",
            "simple_choice",
            sequence=1,
            constr_mandatory=True,
            constr_error_msg="Please select an answer",
            survey_id=survey.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4"},
                {"value": "5"},
            ],
        )
        q_02 = self._add_question(
            None,
            "2x2",
            "simple_choice",
            sequence=2,
            constr_mandatory=True,
            constr_error_msg="Please select an answer",
            survey_id=survey.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4"},
                {"value": "5"},
            ],
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q_01, answer, q_01.suggested_answer_ids[2].id)
        self._add_answer_line(q_02, answer, q_02.suggested_answer_ids[2].id)
        answer.with_user(self.env.user).write({"state": "done"})
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
