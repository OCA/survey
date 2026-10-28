# Copyright 2026 ACSONE SA/NV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

import odoo.tests
from odoo import Command
from odoo.tests.common import HttpCase


@odoo.tests.common.tagged("post_install", "-at_install")
class TestPreventCreateOnStart(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = cls.env["survey.survey"].create(
            {
                "title": "Prevent Create Survey",
                "access_mode": "public",
                "users_login_required": False,
                "prevent_create_on_start": True,
                "question_and_page_ids": [
                    Command.create(
                        {
                            "title": "Question 1",
                            "question_type": "char_box",
                        }
                    )
                ],
            }
        )
        cls.survey_allow = cls.env["survey.survey"].create(
            {
                "title": "Allow Create Survey",
                "access_mode": "public",
                "users_login_required": False,
                "prevent_create_on_start": False,
                "question_and_page_ids": [
                    Command.create(
                        {
                            "title": "Question 1",
                            "question_type": "char_box",
                        }
                    )
                ],
            }
        )

    def test_start_without_token_renders_error_and_does_not_create_answer(self):
        initial_answers_count = self.env["survey.user_input"].search_count(
            [("survey_id", "=", self.survey.id)]
        )
        url = f"/survey/start/{self.survey.access_token}"
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Direct access not allowed", response.text)
        new_answers_count = self.env["survey.user_input"].search_count(
            [("survey_id", "=", self.survey.id)]
        )
        self.assertEqual(new_answers_count, initial_answers_count)

    def test_start_without_token_when_prevent_flag_false_creates_answer(self):
        initial_answers_count = self.env["survey.user_input"].search_count(
            [("survey_id", "=", self.survey_allow.id)]
        )
        url = f"/survey/start/{self.survey_allow.access_token}"
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        new_answers_count = self.env["survey.user_input"].search_count(
            [("survey_id", "=", self.survey_allow.id)]
        )
        self.assertEqual(new_answers_count, initial_answers_count + 1)

    def test_start_with_valid_answer_token_allows_answering(self):
        answer = self.survey._create_answer()
        self.env.cr.flush()
        url = (
            f"/survey/start/{self.survey.access_token}"
            f"?answer_token={answer.access_token}"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Direct access not allowed", response.text)

    def test_start_with_cookie_token_allows_answering(self):
        answer = self.survey._create_answer()
        self.env.cr.flush()
        url = f"/survey/start/{self.survey.access_token}"
        response = self.url_open(
            url, cookies={f"survey_{self.survey.access_token}": answer.access_token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Direct access not allowed", response.text)

    def test_start_with_invalid_survey_token_redirects_with_error(self):
        response = self.url_open(
            "/survey/start/invalid_survey_token", allow_redirects=False
        )
        self.assertEqual(response.status_code, 303)
