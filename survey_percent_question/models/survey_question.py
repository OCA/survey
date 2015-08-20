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


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    type = fields.Selection(
        selection_add=[('percent_split', _('Percentage'))],
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
