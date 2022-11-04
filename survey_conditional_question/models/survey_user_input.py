##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _get_inactive_conditional_questions(self):
        result = super()._get_inactive_conditional_questions()
        questions_to_hide = self.env["survey.question"]
        for question in result:
            if question.triggering_question_type in [
                "simple_choice",
                "multiple_choice",
            ]:
                questions_to_hide |= question
                continue
            question2 = question.triggering_question_id
            input_answer_id = self.user_input_line_ids.filtered(
                lambda x: x.question_id == question2
            )
            if (
                input_answer_id.value_numerical_box < question.conditional_minimum_value
                or input_answer_id.value_numerical_box
                > question.conditional_maximum_value
            ):
                questions_to_hide |= question
        return questions_to_hide
