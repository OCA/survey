from odoo.exceptions import UserError

from .common import TestSurveyUserInputEditCommon


class TestSurveyUserInputEdit(TestSurveyUserInputEditCommon):
    def test_survey_allow_editing_field_default_value(self):
        new_survey = self.env["survey.survey"].create({"title": "Default Survey"})
        self.assertFalse(new_survey.allow_editing)

    def test_can_go_back_when_allow_editing_false_calls_super(self):
        self.survey.allow_editing = False
        self.survey.users_can_go_back = False
        res = self.survey._can_go_back(self.user_input, self.question_2)
        self.assertFalse(res)

    def test_can_go_back_when_users_can_go_back_true_calls_super(self):
        self.survey.allow_editing = True
        self.survey.users_can_go_back = True
        self.user_input.state = "in_progress"
        res = self.survey._can_go_back(self.user_input, self.question_2)
        self.assertTrue(res)

    def test_can_go_back_when_questions_layout_one_page_returns_false(self):
        self.survey.allow_editing = True
        self.survey.users_can_go_back = False
        self.survey.questions_layout = "one_page"
        self.user_input.state = "in_progress"
        res = self.survey._can_go_back(self.user_input, self.question_2)
        self.assertFalse(res)

    def test_can_go_back_when_answer_state_not_in_progress_returns_false(self):
        self.survey.allow_editing = True
        self.survey.users_can_go_back = False
        self.survey.questions_layout = "page_per_question"
        self.user_input.state = "new"
        res = self.survey._can_go_back(self.user_input, self.question_2)
        self.assertFalse(res)

    def test_can_go_back_when_answer_is_session_answer_returns_false(self):
        self.survey.allow_editing = True
        self.survey.users_can_go_back = False
        self.survey.questions_layout = "page_per_question"
        self.user_input.state = "in_progress"
        self.user_input.is_session_answer = True
        res = self.survey._can_go_back(self.user_input, self.question_2)
        self.assertFalse(res)

    def test_can_go_back_when_first_page_of_sections_returns_false(self):
        self.survey.allow_editing = True
        self.survey.users_can_go_back = False
        self.survey.questions_layout = "page_per_section"
        self.user_input.state = "in_progress"
        self.user_input.is_session_answer = False
        section_1 = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "title": "Section 1",
                "is_page": True,
                "sequence": 1,
            }
        )
        self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "title": "Section 2",
                "is_page": True,
                "sequence": 2,
            }
        )
        res = self.survey._can_go_back(self.user_input, section_1)
        self.assertFalse(res)

    def test_can_go_back_when_subsequent_page_of_sections_returns_true(self):
        self.survey.allow_editing = True
        self.survey.users_can_go_back = False
        self.survey.questions_layout = "page_per_section"
        self.user_input.state = "in_progress"
        self.user_input.is_session_answer = False
        self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "title": "Section 1",
                "is_page": True,
                "sequence": 1,
            }
        )
        section_2 = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "title": "Section 2",
                "is_page": True,
                "sequence": 2,
            }
        )
        res = self.survey._can_go_back(self.user_input, section_2)
        self.assertTrue(res)

    def test_can_go_back_when_first_question_in_page_per_question_returns_false(self):
        self.survey.allow_editing = True
        self.survey.users_can_go_back = False
        self.survey.questions_layout = "page_per_question"
        self.survey.question_and_page_ids.filtered(lambda q: q.is_page).unlink()
        self.user_input.state = "in_progress"
        self.user_input.is_session_answer = False
        res = self.survey._can_go_back(self.user_input, self.question_1)
        self.assertFalse(res)

    def test_can_go_back_when_subsequent_question_in_page_per_question_returns_true(
        self,
    ):
        self.survey.allow_editing = True
        self.survey.users_can_go_back = False
        self.survey.questions_layout = "page_per_question"
        self.survey.question_and_page_ids.filtered(lambda q: q.is_page).unlink()
        self.user_input.state = "in_progress"
        self.user_input.is_session_answer = False
        res = self.survey._can_go_back(self.user_input, self.question_2)
        self.assertTrue(res)

    def test_action_reopen_for_edition_resets_state_and_pages(self):
        self.user_input.write(
            {
                "state": "done",
                "last_displayed_page_id": self.question_1.id,
                "survey_first_submitted": True,
            }
        )
        self.user_input.action_reopen_for_edition()
        self.assertEqual(self.user_input.state, "in_progress")
        self.assertFalse(self.user_input.last_displayed_page_id)
        self.assertFalse(self.user_input.survey_first_submitted)

    def test_state_change_tracked_in_chatter(self):
        self.user_input.state = "done"
        self.env.cr.precommit.run()
        initial_msg_count = len(self.user_input.message_ids)
        self.user_input.action_reopen_for_edition()
        self.env.cr.precommit.run()
        tracking_messages = self.user_input.message_ids.filtered(
            lambda m: any(t.field_id.name == "state" for t in m.tracking_value_ids)
        )
        self.assertTrue(len(self.user_input.message_ids) > initial_msg_count)
        self.assertTrue(tracking_messages)

    def test_save_lines_with_allow_editing_forces_overwrite_existing(self):
        self.survey.allow_editing = True
        self.survey.users_can_go_back = False
        self.user_input._save_lines(self.question_1, "Initial Value")
        line = self.user_input.user_input_line_ids.filtered(
            lambda line: line.question_id == self.question_1
        )
        self.assertEqual(line.value_char_box, "Initial Value")
        self.user_input._save_lines(
            self.question_1, "Updated Value", overwrite_existing=False
        )
        lines = self.user_input.user_input_line_ids.filtered(
            lambda line: line.question_id == self.question_1
        )
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines.value_char_box, "Updated Value")

    def test_save_lines_without_allow_editing_raises_when_overwrite_false(self):
        self.survey.allow_editing = False
        self.survey.users_can_go_back = False
        self.user_input._save_lines(
            self.question_1, "Initial Value", overwrite_existing=True
        )
        with self.assertRaisesRegex(UserError, "This answer cannot be overwritten."):
            self.user_input._save_lines(
                self.question_1, "Updated Value", overwrite_existing=False
            )
