from odoo.addons.survey.tests import common


class TestSurveyConditionalQuestions(common.TestSurveyCommon):
    def setUp(self):
        super(TestSurveyConditionalQuestions, self).setUp()
        question = self._add_question(
            self.page_0,
            "Q0",
            "simple_choice",
            survey_id=self.survey.id,
        )
        conditional_question = self._add_question(
            self.page_0,
            "Q0",
            "simple_choice",
            labels=[{"value": 1}, {"value": 2}],
            survey_id=self.survey.id,
        )
        conditional_values = {
            "is_conditional": True,
            "triggering_question_id": question.id,
            "triggering_answer_id": 1,
        }
        conditional_question.write(conditional_values)
        user_input = self.env["survey.user_input"].create(
            {
                "survey_id": question.survey_id.id,
                "partner_id": self.env.user.partner_id.id,
            }
        )
        # Conditional question is hidden when original question not answered
        self.assertIn(conditional_question, user_input.get_hidden_questions())
        tag = "{}_{}".format(question.survey_id.id, question.id)
        conditional_tag = "{}_{}".format(self.survey.id, conditional_question.id)
        self.env["survey.user_input_line"].save_lines(
            user_input.id,
            question,
            {
                "%s_%s"
                % (tag, question.labels_ids[0]["value"]): question.labels_ids[0][
                    "value"
                ]
            },
            tag,
        )
        # Conditional question is not hidden if the desired answer was given
        user_input.refresh()
        self.assertNotIn(conditional_question, user_input.get_hidden_questions())
        data = self.url_open(
            "/survey/hidden/{}/{}/0".format(self.survey.access_token, user_input.token)
        ).json()
        self.assertNotIn(conditional_tag, data["hidden_questions"])
        # Conditional question is hidden for any other answer
        self.env["survey.user_input_line"].save_lines(
            user_input.id,
            question,
            {
                "%s_%s"
                % (tag, question.labels_ids[1]["value"]): question.labels_ids[1][
                    "value"
                ]
            },
            tag,
        )
        user_input.refresh()
        self.assertIn(conditional_question, user_input.get_hidden_questions())

        data = self.url_open(
            "/survey/hidden/{}/{}/0".format(self.survey.access_token, user_input.token)
        ).json()
        self.assertIn(conditional_tag, data["hidden_questions"])
        self.env["survey.user_input_line"].save_lines(
            user_input.id,
            conditional_question,
            {
                conditional_tag: conditional_question.labels_ids[1]["value"],
                "%s_%s"
                % (tag, question.labels_ids[1]["value"]): question.labels_ids[1][
                    "value"
                ],
            },
            conditional_tag,
        )
        user_input.refresh()
        line = user_input.user_input_line_ids.filtered(
            lambda r: r.question_id == conditional_question
        )
        self.assertTrue(line.skipped)
