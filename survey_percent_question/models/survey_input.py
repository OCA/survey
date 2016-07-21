# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, models

from openerp.addons.survey.survey import (
    dict_keys_startswith,
)

from .survey_question import to_decimal


class SurveyInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    @api.model
    def get_old_lines(self, user_input_id, question):
        """ Returns the old input lines """
        return self.search([('user_input_id', '=', user_input_id),
                            ('survey_id', '=', question.survey_id.id),
                            ('question_id', '=', question.id)])

    @api.model
    def save_line_percent_split(self, user_input_id, question, post,
                                answer_tag):
        defaults = {
            "answer_type": "number",
            "user_input_id": user_input_id,
            "question_id": question.id,
            "page_id": question.page_id.id,
            "survey_id": question.survey_id.id,
            "skipped": False
        }

        old_lines = self.get_old_lines(user_input_id, question)
        if old_lines:
            old_lines.unlink()

        answers = dict_keys_startswith(post, answer_tag)
        comment_label = answers.pop(answer_tag + '_comment_label', None)
        comment_value = answers.pop(answer_tag + '_comment_value', None)
        if comment_label:
            comment_value = to_decimal(comment_value)
            self.create(dict(defaults, **{
                "value_number": comment_value,
                "value_text": comment_label,
            }))

        for row in question.labels_ids:
            a_tag = "{0}_{1}".format(answer_tag, row.id)
            self.create(dict(defaults, **{
                "value_number": float(to_decimal(answers.get(a_tag))),
                "value_suggested_row": row.id,
            }))

        return True
