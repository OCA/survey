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

from collections import defaultdict
from decimal import Decimal, InvalidOperation

from openerp import api, fields, models
from openerp.tools.translate import _

from openerp.addons.survey.survey import (
    dict_keys_startswith,
)


def to_decimal(value):
    if value:
        value = value.strip().replace(",", ".")
    else:
        value = '0'

    return Decimal(value)


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


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    type = fields.Selection(
        selection_add=[('percent_split', 'Percentage')],
    )

    @api.model
    def validate_percent_split(self, question, post, answer_tag):
        answers = dict_keys_startswith(post, answer_tag)
        dec_values = []
        comment_label = answers.pop(answer_tag + '_comment_label', None)
        comment_value = answers.get(answer_tag + '_comment_value', None)
        if comment_value and not comment_label:
            return {answer_tag: _(
                "You must provide a label for your extra value"
            )}

        for v in answers.values():
            try:
                dec_values.append(to_decimal(v))
            except InvalidOperation:
                return {answer_tag: _("{0} is not a number").format(v)}

        if not sum(dec_values) == 100:
            return {answer_tag: _(
                'The sum of all values must be 100%, not {0}%'
            ).format(sum(dec_values))}

        return {}


class Survey(models.Model):
    _inherit = 'survey.survey'

    @api.model
    def prepare_result(self, question, current_filters=None):
        '''
        Compute statistical data for questions by counting number of vote per
        choice on basis of filter
        '''
        current_filters = current_filters if current_filters else []
        result_summary = {}

        if question.type == 'percent_split':
            header = []
            order = {}
            idx = 0
            for idx, label in enumerate(question.labels_ids):
                order[label.id] = idx
                header.append(label.value)

            if question.comments_allowed:
                header.extend([_("Other"), _("Comment")])
                order["comment_value"] = idx + 1
                order["comment_label"] = idx + 2

            result_summary["header"] = header

            data = defaultdict(lambda: [''] * len(header))
            all_lines = [
                line
                for line in question.user_input_line_ids
                if not(current_filters) or
                line.user_input_id.id in current_filters
            ]

            for line in all_lines:
                row = data[line.user_input_id]
                if line.value_suggested_row:
                    idx = order[line.value_suggested_row.id]
                    row[idx] = line.value_number
                elif "comment_value" in order:
                    row[order["comment_value"]] = line["value_number"]
                    row[order["comment_label"]] = line["value_text"]
            result_summary["data"] = list(data.values())

        else:
            return super(Survey, self).prepare_result(
                question, current_filters=current_filters)

        return result_summary
