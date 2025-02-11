from odoo.tests import tagged

from odoo.addons.survey.tests.common import TestSurveyCommon


@tagged("-at_install", "post_install", "functional")
class TestCertificationsending(TestSurveyCommon):
    def test_certification_auto_sending(self):
        test_certification = self.env["survey.survey"].create(
            {
                "title": "Test Certification Sending",
                "access_mode": "public",
                "users_login_required": True,
                "questions_layout": "page_per_question",
                "users_can_go_back": True,
                "scoring_type": "scoring_with_answers",
                "scoring_success_min": 85.0,
                "certification": True,
                "certification_mail_template_id": self.env.ref(
                    "survey.mail_template_certification"
                ).id,
                "is_time_limited": True,
                "time_limit": 10,
            }
        )
        q_01 = self._add_question(
            None,
            "2+2",
            "simple_choice",
            sequence=1,
            constr_mandatory=True,
            constr_error_msg="Please select an answer",
            survey_id=test_certification.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4", "is_correct": True, "answer_score": 50.0},
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
            survey_id=test_certification.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4", "is_correct": True, "answer_score": 50.0},
                {"value": "5"},
            ],
        )
        answer = self._add_answer(test_certification, self.env.user)
        self._add_answer_line(q_01, answer, q_01.suggested_answer_ids[2].id)
        self._add_answer_line(q_02, answer, q_02.suggested_answer_ids[2].id)
        answer.with_user(self.env.user).write({"state": "done"})
        answer._mark_done()
        # Verify that the certification has been sent automatically.
        self.assertTrue(answer.scoring_success)
        self.assertTrue(answer.certification_sent)

    def test_certification_skip_auto_sending(self):
        test_certification = self.env["survey.survey"].create(
            {
                "title": "Test Certification Skip Auto Sending",
                "access_mode": "public",
                "users_login_required": True,
                "questions_layout": "page_per_question",
                "users_can_go_back": True,
                "scoring_type": "scoring_with_answers",
                "scoring_success_min": 85.0,
                "certification": True,
                "skip_certification_email": True,
                "certification_mail_template_id": self.env.ref(
                    "survey.mail_template_certification"
                ).id,
                "is_time_limited": True,
                "time_limit": 10,
            }
        )
        q_01 = self._add_question(
            None,
            "2+2",
            "simple_choice",
            sequence=1,
            constr_mandatory=True,
            constr_error_msg="Please select an answer",
            survey_id=test_certification.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4", "is_correct": True, "answer_score": 50.0},
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
            survey_id=test_certification.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4", "is_correct": True, "answer_score": 50.0},
                {"value": "5"},
            ],
        )
        answer = self._add_answer(test_certification, self.env.user)
        self._add_answer_line(q_01, answer, q_01.suggested_answer_ids[2].id)
        self._add_answer_line(q_02, answer, q_02.suggested_answer_ids[2].id)
        answer.with_user(self.env.user).write({"state": "done"})
        answer._mark_done()
        # Verify that the certification has not been sent automatically
        self.assertTrue(answer.scoring_success)
        self.assertFalse(answer.certification_sent)
        # Verify that the certification has been sent manually
        answer.action_manual_send_certification()
        self.assertTrue(answer.certification_sent)

    def test_no_passed_certification_skip_auto_sending(self):
        test_certification = self.env["survey.survey"].create(
            {
                "title": "Test No Passed Certification Skip Auto Sending",
                "access_mode": "public",
                "users_login_required": True,
                "questions_layout": "page_per_question",
                "users_can_go_back": True,
                "scoring_type": "scoring_with_answers",
                "scoring_success_min": 85.0,
                "certification": True,
                "skip_certification_email": True,
                "certification_mail_template_id": self.env.ref(
                    "survey.mail_template_certification"
                ).id,
                "is_time_limited": True,
                "time_limit": 10,
            }
        )
        q_01 = self._add_question(
            None,
            "2+2",
            "simple_choice",
            sequence=1,
            constr_mandatory=True,
            constr_error_msg="Please select an answer",
            survey_id=test_certification.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4", "is_correct": True, "answer_score": 50.0},
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
            survey_id=test_certification.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4", "is_correct": True, "answer_score": 50.0},
                {"value": "5"},
            ],
        )
        answer = self._add_answer(test_certification, self.env.user)
        self._add_answer_line(q_01, answer, q_01.suggested_answer_ids[0].id)
        self._add_answer_line(q_02, answer, q_02.suggested_answer_ids[3].id)
        answer.with_user(self.env.user).write({"state": "done"})
        answer._mark_done()
        # Verify that the certification has not been sent automatically
        self.assertFalse(answer.scoring_success)
        self.assertFalse(answer.certification_sent)
        # Verify that the certification has not been sent manually
        answer.action_manual_send_certification()
        self.assertFalse(answer.certification_sent)
