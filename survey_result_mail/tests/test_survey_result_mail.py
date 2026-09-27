# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import datetime
from unittest.mock import patch

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

    # --- shared helper ---

    def _make_result_survey(self, title, extra_vals=None):
        vals = {
            "title": title,
            "access_mode": "public",
            "users_login_required": True,
            "send_result_mail": True,
        }
        if extra_vals:
            vals.update(extra_vals)
        return self.env["survey.survey"].create(vals)

    # --- _mark_done branches ---

    def test_mark_done_no_send_result_mail(self):
        survey = self._make_result_survey(
            "No Send", extra_vals={"send_result_mail": False}
        )
        q = self._add_question(
            None,
            "Q1",
            "simple_choice",
            sequence=1,
            survey_id=survey.id,
            labels=[{"value": "A"}, {"value": "B"}],
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q, answer, q.suggested_answer_ids[0].id)
        answer.write({"state": "done"})
        answer._mark_done()
        mail = self.env["mail.message"].search(
            [
                ("res_id", "=", answer.id),
                ("model", "=", "survey.user_input"),
                ("subject", "ilike", "Results for"),
            ]
        )
        self.assertFalse(mail)

    def test_mark_done_no_email(self):
        survey = self._make_result_survey("No Email Survey")
        q = self._add_question(
            None,
            "Q1",
            "simple_choice",
            sequence=1,
            survey_id=survey.id,
            labels=[{"value": "A"}, {"value": "B"}],
        )
        # partner=False, email=False → filtered out in _mark_done
        answer = self._add_answer(survey, False)
        self._add_answer_line(q, answer, q.suggested_answer_ids[0].id)
        answer.write({"state": "done"})
        answer._mark_done()
        mail = self.env["mail.message"].search(
            [
                ("res_id", "=", answer.id),
                ("model", "=", "survey.user_input"),
                ("subject", "ilike", "Results for"),
            ]
        )
        self.assertFalse(mail)

    def test_mark_done_custom_template(self):
        model_id = (
            self.env["ir.model"]
            .search([("model", "=", "survey.user_input")], limit=1)
            .id
        )
        custom_template = self.env["mail.template"].create(
            {
                "name": "Custom Survey Results",
                "model_id": model_id,
                "subject": "Custom Results for {{ object.survey_id.title }}",
                "body_html": "<p>Your custom results</p>",
                "email_to": "{{ object.partner_id.email or object.email or '' }}",
            }
        )
        survey = self._make_result_survey(
            "Custom Template Survey",
            extra_vals={"result_mail_template_id": custom_template.id},
        )
        q = self._add_question(
            None,
            "Q1",
            "simple_choice",
            sequence=1,
            survey_id=survey.id,
            labels=[{"value": "A"}, {"value": "B"}],
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q, answer, q.suggested_answer_ids[0].id)
        answer.write({"state": "done"})
        answer._mark_done()
        mail = self.env["mail.message"].search(
            [
                ("res_id", "=", answer.id),
                ("model", "=", "survey.user_input"),
                ("subject", "ilike", "Custom Results for"),
            ]
        )
        self.assertTrue(mail)

    # --- _build_answers_html branches ---

    def test_build_answers_html_char_and_simple_choice(self):
        survey = self._make_result_survey("Build Answers HTML")
        q_char = self._add_question(
            None, "Full Name", "char_box", sequence=1, survey_id=survey.id
        )
        q_sc = self._add_question(
            None,
            "Favorite color",
            "simple_choice",
            sequence=2,
            survey_id=survey.id,
            labels=[{"value": "Red"}, {"value": "Blue"}],
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q_char, answer, "Alice")
        self._add_answer_line(q_sc, answer, q_sc.suggested_answer_ids[0].id)
        html = answer._build_answers_html()
        self.assertIn("Alice", html)
        self.assertIn("Red", html)

    def test_build_answers_html_date_datetime(self):
        survey = self._make_result_survey("Date Datetime HTML")
        q_date = self._add_question(
            None, "Survey date", "date", sequence=1, survey_id=survey.id
        )
        q_dt = self._add_question(
            None, "Exact moment", "datetime", sequence=2, survey_id=survey.id
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q_date, answer, datetime.date(2024, 6, 15))
        self._add_answer_line(q_dt, answer, datetime.datetime(2024, 6, 15, 10, 30, 0))
        html = answer._build_answers_html()
        # Both question titles must appear; confirms date/datetime code paths ran
        self.assertIn("Survey date", html)
        self.assertIn("Exact moment", html)

    def test_build_answers_html_multiple_choice(self):
        survey = self._make_result_survey("Multiple Choice HTML")
        q_mc = self._add_question(
            None,
            "Languages",
            "multiple_choice",
            sequence=1,
            survey_id=survey.id,
            labels=[
                {"value": "Python"},
                {"value": "JavaScript"},
                {"value": "Go"},
            ],
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q_mc, answer, q_mc.suggested_answer_ids[0].id)
        self._add_answer_line(q_mc, answer, q_mc.suggested_answer_ids[1].id)
        html = answer._build_answers_html()
        self.assertIn("Python", html)
        self.assertIn("JavaScript", html)

    def test_build_answers_html_matrix(self):
        survey = self._make_result_survey("Matrix HTML")
        q_mx = self._add_question(
            None,
            "Harvest season",
            "matrix",
            sequence=1,
            survey_id=survey.id,
            labels=[{"value": "Spring"}, {"value": "Summer"}],
            labels_2=[{"value": "Apples"}, {"value": "Strawberries"}],
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(
            q_mx,
            answer,
            q_mx.suggested_answer_ids[0].id,
            answer_value_row=q_mx.matrix_row_ids[0].id,
        )
        html = answer._build_answers_html()
        self.assertIn("Harvest season", html)
        self.assertIn("Apples", html)
        self.assertIn("Spring", html)

    def test_build_answers_html_unknown_type_is_skipped(self):
        """Answer lines whose answer_type has no value_<type> field are silently
        skipped; the rest of the result still renders without error."""
        survey = self._make_result_survey("Unknown Answer Type")
        q_known = self._add_question(
            None, "Date question", "date", sequence=1, survey_id=survey.id
        )
        q_unknown = self._add_question(
            None, "Custom type question", "char_box", sequence=2, survey_id=survey.id
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q_known, answer, datetime.date(2024, 1, 1))
        self._add_answer_line(q_unknown, answer, "should not appear")
        # Simulate a custom answer_type with no matching value_<type> field by
        # hiding value_char_box from _fields (mirrors e.g. survey_question_type_binary)
        line_cls = type(self.env["survey.user_input.line"])
        patched_fields = {
            k: v for k, v in line_cls._fields.items() if k != "value_char_box"
        }
        with patch.object(line_cls, "_fields", patched_fields):
            html = answer._build_answers_html()
        self.assertIn("Date question", html)
        self.assertNotIn("Custom type question", html)
        self.assertNotIn("should not appear", html)

    def test_build_answers_html_skipped_excluded(self):
        survey = self._make_result_survey("Skipped HTML")
        q_answered = self._add_question(
            None, "Answered question", "char_box", sequence=1, survey_id=survey.id
        )
        q_skipped = self._add_question(
            None, "Skipped question", "char_box", sequence=2, survey_id=survey.id
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q_answered, answer, "Hello")
        # answer_type=False required: constraint rejects skipped=True + any answer_type
        self._add_answer_line(q_skipped, answer, False, answer_type=False, skipped=True)
        html = answer._build_answers_html()
        self.assertIn("Hello", html)
        self.assertNotIn("Skipped question", html)

    # --- _compute_survey_result modes ---

    def test_compute_survey_result_basic_mode(self):
        survey = self._make_result_survey("Basic Mode")
        q = self._add_question(
            None, "Feeling today", "char_box", sequence=1, survey_id=survey.id
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q, answer, "Great")
        html = answer.with_context(survey_result_mode="basic").survey_result
        self.assertIn("Great", html)

    def test_compute_survey_result_bootstrap_mode(self):
        # Mock ir.ui.view._render_template (not _render_user_input) so the full
        # body of _render_user_input is executed and covered, while avoiding the
        # web.layout render that requires an HTTP request context.
        survey = self._make_result_survey("Bootstrap Mode")
        q = self._add_question(
            None,
            "Pick one",
            "simple_choice",
            sequence=1,
            survey_id=survey.id,
            labels=[{"value": "Option A"}, {"value": "Option B"}],
        )
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q, answer, q.suggested_answer_ids[0].id)
        answer.write({"state": "done"})
        with patch.object(
            type(self.env["ir.ui.view"]),
            "_render_template",
            return_value="<p>bootstrap rendered</p>",
        ):
            html = answer.with_context(survey_result_mode="bootstrap").survey_result
        self.assertTrue(html)

    def test_compute_survey_result_unknown_mode(self):
        # covers: elif mode == "basic" → False branch (mode is neither bootstrap
        # nor basic — both if/elif evaluate to False, survey_result stays empty)
        survey = self._make_result_survey("Unknown Mode")
        q = self._add_question(None, "Q1", "char_box", sequence=1, survey_id=survey.id)
        answer = self._add_answer(survey, self.env.user)
        self._add_answer_line(q, answer, "something")
        html = answer.with_context(survey_result_mode="unknown").survey_result
        self.assertFalse(html)
