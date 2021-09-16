from odoo.tests.common import TransactionCase


class TestSurveyConditionalQuestions(TransactionCase):
    def test_survey_conditional_questions(self):
        label = self.env.ref("survey.choice_1_1_1")
        question = label.question_id
        survey = question.survey_id

        conditional_question = survey.page_ids[1].question_ids[0]
        conditional_values = {
            "is_conditional": True,
            "triggering_question_id": question.id,
            "triggering_answer_id": label.id,
        }
        conditional_question.write(conditional_values)
        user_input = self.env["survey.user_input"].create(
            {"survey_id": survey.id, "partner_id": self.env.user.partner_id.id,}
        )

        # Conditional question is hidden when original question not answered
        self.assertIn(conditional_question, user_input.get_hidden_questions())
        input_line = self.env["survey.user_input_line"].create(
            {
                "answer_type": "suggestion",
                "question_id": question.id,
                "skipped": False,
                "user_input_id": user_input.id,
                "value_suggested": label.id,
            }
        )

        # Conditional question is not hidden if the desired answer was given
        self.assertNotIn(conditional_question, user_input.get_hidden_questions())

        # Conditional question is hidden for any other answer
        input_line.value_suggested = self.env.ref("survey.choice_1_1_2")
        self.assertIn(conditional_question, user_input.get_hidden_questions())

        # Next page returns the next page
        self.assertEqual(
            survey.next_page(user_input, survey.page_ids[0].id)[0], survey.page_ids[1]
        )

        # Hide all the questions on the page
        survey.page_ids[1].question_ids.write(conditional_values)
        # Next page skips the next page
        self.assertEqual(
            survey.next_page(user_input, survey.page_ids[0].id)[0], survey.page_ids[2]
        )
        # In both directions
        self.assertEqual(
            survey.next_page(user_input, survey.page_ids[2].id, go_back=True)[0],
            survey.page_ids[0],
        )
