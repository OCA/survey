# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class SurveyUserInputLine(models.Model):

    _inherit = 'survey.user_input_line'

    @api.model
    def save_line_star_rate(self, user_input_id, question, post, answer_tag):
        vals = {
            'user_input_id': user_input_id,
            'question_id': question.id,
            'survey_id': question.survey_id.id,
            'skipped': False,
        }
        if answer_tag in post and post[answer_tag].strip():
            vals.update(
                {
                    'answer_type': 'number',
                    'value_number': float(post[answer_tag]),
                }
            )
        else:
            vals.update({'answer_type': None, 'skipped': True})
        old_uil = self.search(
            [
                ('user_input_id', '=', user_input_id),
                ('survey_id', '=', question.survey_id.id),
                ('question_id', '=', question.id),
            ]
        )
        if old_uil:
            old_uil.write(vals)
        else:
            old_uil.create(vals)
        return True

    @api.multi
    @api.constrains('question_id', 'answer_type', 'value_number')
    def _check_star_rate_answer(self):
        for rec in self:
            if rec.question_id.type == 'star_rate':
                if rec.answer_type != 'number':
                    raise ValidationError(
                        _("Five stars rate question must have numeric answer")
                    )
                if rec.question_id.constr_mandatory and not (
                    0 < rec.value_number <= 5
                ):
                    raise ValidationError(
                        _("Answer is not in the right range")
                    )
                if not rec.question_id.constr_mandatory and not (
                    0 <= rec.value_number <= 5
                ):
                    raise ValidationError(
                        _("Answer is not in the right range")
                    )
