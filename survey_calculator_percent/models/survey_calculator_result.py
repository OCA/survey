# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
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

from openerp import models


class SurveyCalculatorResult(models.Model):
    _inherit = 'survey.calculator.result'

    def add_answer(self, answers, user_input_line):
        """
        Add percentage user_input_line in 'answers' dictionary.

        - for percentage questions:
        answers[id] contains a dictionary which keys are the ids of
        survey.label rows and the values are the percentages chosen.
        """
        question = user_input_line.question_id
        qtype = question.type
        qid = question.id
        if qtype == 'percent_split':
            if qid not in answers:
                answers[qid] = {}
            row_id = user_input_line.value_suggested_row.id
            answers[qid][row_id] = user_input_line.value_number
        else:
            super(SurveyCalculatorResult, self).add_answer(
                answers, user_input_line
            )
