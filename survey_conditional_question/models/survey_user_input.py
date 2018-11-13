##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    @api.model
    def get_list_questions(self, survey, user_input):
        obj_questions = self.env['survey.question']
        questions_to_hide = []
        question_ids = obj_questions.search(
            [('survey_id', '=', survey.id)])
        for question in question_ids.filtered('conditional'):
            for question2 in question_ids.filtered(
                    lambda x: x == question.question_conditional_id):
                input_answer_ids = user_input.user_input_line_ids.filtered(
                    lambda x: x.question_id == question2)
                for answers in input_answer_ids.filtered(
                        lambda x: x.value_suggested != question.answer_id):
                    questions_to_hide.append(question.id)
        return questions_to_hide
