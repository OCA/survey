# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase


class TestSurveyAnswerGeneration(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey1 = cls.env["survey.survey"].create(
            {"title": "Survey 1", "access_mode": "public"}
        )
        cls.survey2 = cls.env["survey.survey"].create(
            {"title": "Survey 2", "access_mode": "public"}
        )
        cls.survey1.next_survey_id = cls.survey2

        cls.text_q1 = cls.env["survey.question"].create(
            {
                "title": "Describe yourself",
                "survey_id": cls.survey1.id,
                "question_type": "char_box",
                "sequence": 1,
            }
        )
        cls.text_q2 = cls.env["survey.question"].create(
            {
                "title": "Describe yourself",
                "survey_id": cls.survey2.id,
                "question_type": "char_box",
                "sequence": 1,
            }
        )
        cls.text_q1.next_survey_question_id = cls.text_q2

        cls.choice_q1 = cls.env["survey.question"].create(
            {
                "title": "Choose an option",
                "survey_id": cls.survey1.id,
                "question_type": "simple_choice",
                "sequence": 2,
            }
        )
        cls.choice_q2 = cls.env["survey.question"].create(
            {
                "title": "Choose an option",
                "survey_id": cls.survey2.id,
                "question_type": "simple_choice",
                "sequence": 2,
            }
        )
        cls.choice_q1.next_survey_question_id = cls.choice_q2

        cls.option_a1 = cls.env["survey.question.answer"].create(
            {"question_id": cls.choice_q1.id, "value": "Option A"}
        )
        cls.option_a2 = cls.env["survey.question.answer"].create(
            {"question_id": cls.choice_q2.id, "value": "Option A"}
        )
        cls.option_a1.next_survey_question_answer_id = cls.option_a2

        cls.partner = cls.env["res.partner"].create({"name": "Test User"})

    def _create_input(self, survey, **kwargs):
        return survey._create_answer(test_entry=True, **kwargs)

    def test_create_answer_creates_linked_input(self):
        """Creating an answer for survey1 also creates a linked input for survey2."""
        input1 = self._create_input(self.survey1)
        self.assertTrue(input1.next_survey_input_id)
        self.assertEqual(input1.next_survey_input_id.survey_id, self.survey2)
        self.assertEqual(input1.next_survey_input_id.origin_input_id, input1)

    def test_create_answer_no_next_survey(self):
        """Creating an answer for a survey with no next_survey_id has no linked
        input."""
        input2 = self._create_input(self.survey2)
        self.assertFalse(input2.next_survey_input_id)

    def test_save_text_answer_syncs_to_next_survey(self):
        """Saving a char_box answer in survey1 pre-fills the linked question in
        survey2."""
        input1 = self._create_input(self.survey1)
        input1._save_lines(self.text_q1, "Hello OCA")
        next_input = input1.next_survey_input_id
        synced_line = next_input.user_input_line_ids.filtered(
            lambda line: line.question_id == self.text_q2
        )
        self.assertTrue(synced_line)
        self.assertEqual(synced_line.value_char_box, "Hello OCA")

    def test_save_suggestion_answer_syncs_to_next_survey(self):
        """Saving a choice answer in survey1 pre-fills the mapped option in survey2."""
        input1 = self._create_input(self.survey1)
        input1._save_lines(self.choice_q1, self.option_a1.id)
        next_input = input1.next_survey_input_id
        synced_line = next_input.user_input_line_ids.filtered(
            lambda line: line.question_id == self.choice_q2
        )
        self.assertTrue(synced_line)
        self.assertEqual(synced_line.suggested_answer_id, self.option_a2)

    def test_save_lines_without_linked_question_does_not_sync(self):
        """Answers to questions without next_survey_question_id are not synced."""
        unlinked_q = self.env["survey.question"].create(
            {
                "title": "Unlinked question",
                "survey_id": self.survey1.id,
                "question_type": "char_box",
                "sequence": 3,
            }
        )
        input1 = self._create_input(self.survey1)
        input1._save_lines(unlinked_q, "should not sync")
        next_input = input1.next_survey_input_id
        self.assertFalse(next_input.user_input_line_ids)

    def test_diff_with_origin_computed_on_change(self):
        """When a pre-filled answer is changed in survey2, the diff is computed."""
        input1 = self._create_input(self.survey1)
        input1._save_lines(self.text_q1, "Original answer")
        next_input = input1.next_survey_input_id
        synced_line = next_input.user_input_line_ids.filtered(
            lambda line: line.question_id == self.text_q2
        )
        # Simulate user changing the pre-filled answer in survey2
        synced_line.value_char_box = "Changed answer"
        self.assertTrue(synced_line.diff_with_origin)

    def test_diff_with_origin_empty_when_unchanged(self):
        """When the pre-filled answer is not changed, no diff is shown."""
        input1 = self._create_input(self.survey1)
        input1._save_lines(self.text_q1, "Same answer")
        next_input = input1.next_survey_input_id
        synced_line = next_input.user_input_line_ids.filtered(
            lambda line: line.question_id == self.text_q2
        )
        self.assertFalse(synced_line.diff_with_origin)

    def test_mark_done_syncs_partner_to_next_survey(self):
        """Completing survey1 updates the partner on the linked survey2 input."""
        input1 = self._create_input(self.survey1, partner=self.partner)
        next_input = input1.next_survey_input_id
        self.assertFalse(next_input.partner_id)
        input1._mark_done()
        self.assertEqual(next_input.partner_id, self.partner)

    def test_diff_line_count_computed(self):
        """diff_user_input_line_count reflects the number of lines with diffs."""
        input1 = self._create_input(self.survey1)
        input1._save_lines(self.text_q1, "Original")
        next_input = input1.next_survey_input_id
        synced_line = next_input.user_input_line_ids.filtered(
            lambda line: line.question_id == self.text_q2
        )
        self.assertEqual(next_input.diff_user_input_line_count, 0)
        synced_line.value_char_box = "Modified"
        next_input._compute_diff_user_input_line_count()
        self.assertEqual(next_input.diff_user_input_line_count, 1)
