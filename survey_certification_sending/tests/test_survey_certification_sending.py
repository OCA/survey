# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from unittest.mock import patch

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

    def test_certification_partner_skip_auto_sending(self):
        test_certification = self.env["survey.survey"].create(
            {
                "title": "Test Partner Skip Auto Sending",
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
        # Set on answer.partner_id to ensure it applies to the actual partner
        # used in the test
        answer.partner_id.write({"skip_certification_email": True})
        answer.with_user(self.env.user).write({"state": "done"})
        answer._mark_done()
        # Verify that the certification has not been sent automatically
        self.assertTrue(answer.scoring_success)
        self.assertFalse(answer.certification_sent)
        # Verify that the certification has been sent manually
        answer.action_manual_send_certification()
        self.assertTrue(answer.certification_sent)

    # --- shared helper ---

    def _make_passing_certification(self, title, extra_vals=None):
        vals = {
            "title": title,
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
        }
        if extra_vals:
            vals.update(extra_vals)
        survey = self.env["survey.survey"].create(vals)
        q = self._add_question(
            None,
            "1+1",
            "simple_choice",
            sequence=1,
            constr_mandatory=True,
            constr_error_msg="Please select an answer",
            survey_id=survey.id,
            labels=[
                {"value": "1"},
                {"value": "2", "is_correct": True, "answer_score": 100.0},
            ],
        )
        return survey, q

    # --- survey_user_input.py coverage ---

    def test_mark_done_test_entry_skips_certification(self):
        survey, q = self._make_passing_certification("Test Entry No Cert")
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q, answer, q.suggested_answer_ids[1].id)
        answer.write({"test_entry": True, "state": "done"})
        answer._mark_done()
        self.assertTrue(answer.scoring_success)
        self.assertFalse(answer.certification_sent)

    def test_mark_done_no_template_skips_certification(self):
        survey, q = self._make_passing_certification(
            "No Template No Cert",
            extra_vals={"certification_mail_template_id": False},
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q, answer, q.suggested_answer_ids[1].id)
        answer.write({"state": "done"})
        answer._mark_done()
        self.assertTrue(answer.scoring_success)
        self.assertFalse(answer.certification_sent)

    def test_manual_send_success_notification(self):
        survey, q = self._make_passing_certification(
            "Manual Send Success", extra_vals={"skip_certification_email": True}
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q, answer, q.suggested_answer_ids[1].id)
        answer.write({"state": "done"})
        answer._mark_done()
        result = answer.action_manual_send_certification()
        self.assertEqual(result["type"], "ir.actions.client")
        self.assertEqual(result["params"]["type"], "success")
        self.assertTrue(answer.certification_sent)

    def test_manual_send_warning_when_not_passed(self):
        survey, q = self._make_passing_certification("Manual Send Warning")
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q, answer, q.suggested_answer_ids[0].id)
        answer.write({"state": "done"})
        answer._mark_done()
        result = answer.action_manual_send_certification()
        self.assertEqual(result["type"], "ir.actions.client")
        self.assertEqual(result["params"]["type"], "warning")
        self.assertFalse(answer.certification_sent)

    def test_manual_send_no_template_returns_warning(self):
        # covers: if template: False branch — answer passed but no template set
        survey, q = self._make_passing_certification(
            "Manual Send No Template",
            extra_vals={"certification_mail_template_id": False},
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q, answer, q.suggested_answer_ids[1].id)
        answer.write({"state": "done"})
        answer._mark_done()
        result = answer.action_manual_send_certification()
        self.assertEqual(result["type"], "ir.actions.client")
        self.assertEqual(result["params"]["type"], "warning")
        self.assertFalse(answer.certification_sent)

    # --- mail_template.py coverage ---

    def test_send_mail_non_survey_model_calls_super(self):
        # This module overrides send_mail on ALL mail.template records.
        # The guard "if self.model == 'survey.user_input'" ensures the skip
        # logic never interferes with templates for other models.
        # This test covers the False branch of that guard.
        model_id = (
            self.env["ir.model"].search([("model", "=", "res.partner")], limit=1).id
        )
        partner_template = self.env["mail.template"].create(
            {
                "name": "Test Non Survey Template",
                "model_id": model_id,
                "subject": "Test",
                "body_html": "<p>Test</p>",
            }
        )
        with patch(
            "odoo.addons.mail.models.mail_template.MailTemplate.send_mail",
            return_value=True,
        ) as mock_send:
            result = partner_template.send_mail(self.env.user.partner_id.id)
            mock_send.assert_called_once()
        self.assertTrue(result)

    def test_send_mail_returns_false_when_survey_skip(self):
        survey, _q = self._make_passing_certification(
            "Send Mail Survey Skip",
            extra_vals={"skip_certification_email": True},
        )
        answer = self._add_answer(survey, self.env.user)
        template = self.env.ref("survey.mail_template_certification")
        self.assertFalse(template.send_mail(answer.id))

    def test_send_mail_returns_false_when_partner_skip(self):
        survey, _q = self._make_passing_certification("Send Mail Partner Skip")
        answer = self._add_answer(survey, self.env.user)
        answer.partner_id.write({"skip_certification_email": True})
        template = self.env.ref("survey.mail_template_certification")
        self.assertFalse(template.send_mail(answer.id))

    def test_send_mail_proceeds_when_no_skip(self):
        survey, _q = self._make_passing_certification("Send Mail Proceeds")
        answer = self._add_answer(survey, self.env.user)
        template = self.env.ref("survey.mail_template_certification")
        with patch(
            "odoo.addons.mail.models.mail_template.MailTemplate.send_mail",
            return_value=True,
        ) as mock_send:
            result = template.send_mail(answer.id)
            mock_send.assert_called_once()
        self.assertTrue(result)
