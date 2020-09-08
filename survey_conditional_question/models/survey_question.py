##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    is_conditional = fields.Boolean(
        'Conditional Question',
        copy=False,
        # we add copy = false to avoid wrong link on survey copy,
        # should be improoved
    )
    triggering_question_id = fields.Many2one(
        'survey.question',
        'Question',
        copy=False,
        help="In order to edit this field you should"
             " first save the question"
    )
    triggering_answer_id = fields.Many2one(
        'survey.label',
        'Answer',
        copy=False,
    )

    @api.multi
    def validate_question(self, post, answer_tag):
        """ Skip validation of hidden questions """
        self.ensure_one()
        if self.triggering_question_id:
            input_answer_ids = self.env['survey.user_input_line'].search(
                [('user_input_id.token', '=', post.get('token')),
                 ('question_id', '=', self.triggering_question_id.id)])
            for answers in input_answer_ids:
                value_suggested = answers.value_suggested
                if (self.is_conditional and
                        self.triggering_answer_id != value_suggested):
                    return {}
        return super(SurveyQuestion, self).validate_question(post, answer_tag)
