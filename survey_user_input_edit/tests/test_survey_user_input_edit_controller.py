import odoo.tests
from odoo.tests.common import HttpCase

from .common import TestSurveyUserInputEditCommon


@odoo.tests.common.tagged("post_install", "-at_install")
class TestSurveyUserInputEditController(TestSurveyUserInputEditCommon, HttpCase):
    def test_survey_start_with_done_answer_and_edit_flag_reopens_answer(self):
        self.user_input.state = "done"
        url = (
            f"/survey/start/{self.survey.access_token}?"
            f"answer_token={self.user_input.access_token}&edit=1"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.user_input.invalidate_recordset(["state"])
        self.assertEqual(self.user_input.state, "in_progress")

    def test_survey_start_with_done_answer_without_edit_flag_keeps_done_state(self):
        self.user_input.state = "done"
        url = (
            f"/survey/start/{self.survey.access_token}?"
            f"answer_token={self.user_input.access_token}"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.user_input.invalidate_recordset(["state"])
        self.assertEqual(self.user_input.state, "done")

    def test_survey_start_with_done_answer_and_allow_editing_false_keeps_done_state(
        self,
    ):
        self.survey.allow_editing = False
        self.user_input.state = "done"
        url = (
            f"/survey/start/{self.survey.access_token}?"
            f"answer_token={self.user_input.access_token}&edit=1"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.user_input.invalidate_recordset(["state"])
        self.assertEqual(self.user_input.state, "done")

    def test_survey_start_with_cookie_and_edit_flag_reopens_answer(self):
        self.survey.allow_editing = True
        self.user_input.state = "done"
        self.opener.cookies.set(
            f"survey_{self.survey.access_token}", self.user_input.access_token
        )
        url = f"/survey/start/{self.survey.access_token}?edit=1"
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.user_input.invalidate_recordset(["state"])
        self.assertEqual(self.user_input.state, "in_progress")

    def test_survey_start_with_invalid_cookie_token_falls_back_without_token(self):
        self.survey.allow_editing = True
        self.opener.cookies.set(
            f"survey_{self.survey.access_token}", "non_existent_token"
        )
        response = self.url_open(f"/survey/start/{self.survey.access_token}")
        self.assertEqual(response.status_code, 200)

    def test_survey_start_with_invalid_survey_token_redirects_with_error(self):
        response = self.url_open(
            "/survey/start/invalid_survey_token", allow_redirects=False
        )
        self.assertEqual(response.status_code, 303)

    def test_survey_start_with_logged_in_user_and_edit_flag_reopens_existing_answer(
        self,
    ):
        self.survey.allow_editing = True
        admin = self.env.ref("base.user_admin")
        self.user_input.write({"partner_id": admin.partner_id.id, "state": "done"})
        self.env.cr.flush()
        self.authenticate(admin.login, admin.login)
        url = f"/survey/start/{self.survey.access_token}?edit=1"
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.user_input.invalidate_recordset(["state"])
        self.assertEqual(self.user_input.state, "in_progress")

    def test_survey_start_with_logged_in_user_without_edit_flag_keeps_done_state(self):
        self.survey.allow_editing = True
        admin = self.env.ref("base.user_admin")
        self.user_input.write({"partner_id": admin.partner_id.id, "state": "done"})
        self.env.cr.flush()
        self.authenticate(admin.login, admin.login)
        url = f"/survey/start/{self.survey.access_token}"
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.user_input.invalidate_recordset(["state"])
        self.assertEqual(self.user_input.state, "done")

    def test_survey_start_with_public_user_creates_new_answer(self):
        self.survey.allow_editing = True
        self.user_input.state = "done"
        self.authenticate(None, None)
        self.opener.cookies.clear()
        count_before = self.env["survey.user_input"].search_count(
            [("survey_id", "=", self.survey.id)]
        )
        response = self.url_open(f"/survey/start/{self.survey.access_token}")
        self.assertEqual(response.status_code, 200)
        self.user_input.invalidate_recordset(["state"])
        self.assertEqual(self.user_input.state, "done")
        count_after = self.env["survey.user_input"].search_count(
            [("survey_id", "=", self.survey.id)]
        )
        self.assertEqual(count_after, count_before + 1)

    def test_survey_display_page_with_edit_flag_and_answer_token_redirects_to_start(
        self,
    ):
        self.survey.allow_editing = True
        self.user_input.state = "done"
        url = (
            f"/survey/{self.survey.access_token}/{self.user_input.access_token}?edit=1"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.user_input.invalidate_recordset(["state"])
        self.assertEqual(self.user_input.state, "in_progress")

    def test_survey_display_page_with_edit_flag_and_cookie_redirects_to_start(self):
        self.survey.allow_editing = True
        self.user_input.state = "done"
        self.opener.cookies.set(
            f"survey_{self.survey.access_token}", self.user_input.access_token
        )
        url = f"/survey/{self.survey.access_token}?edit=1"
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.user_input.invalidate_recordset(["state"])
        self.assertEqual(self.user_input.state, "in_progress")

    def test_survey_display_page_with_edit_flag_without_token_calls_super(self):
        self.survey.allow_editing = True
        self.authenticate(None, None)
        self.opener.cookies.clear()
        response = self.url_open(
            f"/survey/{self.survey.access_token}?edit=1", allow_redirects=False
        )
        self.assertEqual(response.status_code, 303)
        self.assertTrue(response.headers.get("Location", "").endswith("/"))

    def test_survey_display_page_without_edit_flag_calls_super(self):
        self.survey.allow_editing = True
        self.user_input.state = "done"
        url = f"/survey/{self.survey.access_token}/{self.user_input.access_token}"
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.user_input.invalidate_recordset(["state"])
        self.assertEqual(self.user_input.state, "done")
