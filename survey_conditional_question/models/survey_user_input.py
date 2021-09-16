##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    @api.model
    def get_hidden_questions(self):
        """ Return the questions that should be hidden based on the current
        user input """
        questions_to_hide = self.env["survey.question"]
        questions = self.survey_id.mapped("question_ids")
        for question in questions.filtered("is_conditional"):
            question2 = question.triggering_question_id
            input_answer_id = self.user_input_line_ids.filtered(
                lambda x: x.question_id == question2
            )
            if question2.question_type in [
                "simple_choice",
                "multiple_choice",
            ] and question.triggering_answer_id not in (
                input_answer_id.mapped("value_suggested")
            ):
                questions_to_hide |= question
            elif (
                input_answer_id.value_number < question.conditional_minimum_value
                or input_answer_id.value_number > question.conditional_maximum_value
            ):
                questions_to_hide |= question
        return questions_to_hide
