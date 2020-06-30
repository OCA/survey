# Copyright 2020 Le Filament (<https://www.le-filament.com>)
# License GPL-3.0 or later (https://www.gnu.org/licenses/gpl).

from odoo import models


class Survey(models.Model):
    _inherit = 'survey.survey'

    def copy(self, default=None):
        res = super(Survey, self).copy(default)
        for page in res.page_ids:
            for question in page.question_ids:
                if question.conditional:
                    new_conditional_question_id = question.search([
                        ['page_id', '=', question.page_id.id],
                        ['question', '=',
                         question.conditional_question_id.question]
                    ])
                    new_conditional_option_id = res.env['survey.label'].search(
                        [['question_id', '=', new_conditional_question_id.id],
                         ['value', '=', question.conditional_option_id.value]])
                    question.write({
                        'conditional_question_id':
                            new_conditional_question_id.id,
                        'conditional_option_id': new_conditional_option_id.id
                    })
        return res
