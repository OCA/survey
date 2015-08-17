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

from openerp import api, models, fields
from openerp.tools import ustr
from openerp.tools.safe_eval import safe_eval


class SurveyCalculatorResult(models.Model):
    _name = 'survey.calculator.result'
    _description = "Survey Calculator Result"

    user_input_id = fields.Many2one(
        'survey.user_input',
        'User Input',
        required=True,
        help='The user input (answers) on which the calculation will be '
             'applied.',
        domain='[("state", "=", "done")]'
    )
    partner_id = fields.Many2one(
        'res.partner',
        'Partner',
        related='user_input_id.partner_id.parent_id',
        readonly=True,
        store=True,
    )
    survey_id = fields.Many2one(
        'survey.survey',
        'Survey',
        related='user_input_id.survey_id',
        readonly=True,
        help='Survey used to compute results',
        store=True,
    )
    computation_id = fields.Many2one(
        'survey.calculator.computation',
        'Computation',
        required=True,
        help="The computation that will be applied on the "
             "survey answers.",
        domain='[("survey_id", "=", survey_id)]',
    )
    result = fields.Float(
        'Result',
        readonly=True,
        help='Result of the calculation',
        compute='compute_results',
    )
    tag = fields.Char(
        'Tag',
        readonly=True,
        help='Tag obtained in the computation',
        compute='compute_results'
    )

    def add_answer(self, answers, user_input_line):
        """
        Add the answer of the given user_input_line in 'answers' dictionary.
        """
        question = user_input_line.question_id
        qtype = question.type
        qid = question.id
        if qtype == 'free_text':
            answers[qid] = user_input_line.value_free_text
        elif qtype == 'textbox':
            answers[qid] = user_input_line.value_text
        elif qtype == 'numerical_box':
            answers[qid] = user_input_line.value_number
        elif qtype == 'datetime':
            answers[qid] = user_input_line.value_date
        elif qtype == 'simple_choice':
            answers[qid] = user_input_line.value_suggested.id
        elif qtype == 'multiple_choice':
            if qid not in answers:
                answers[qid] = []
            answers[qid].append(user_input_line.value_suggested.id)
        elif qtype == 'matrix':
            row_id = user_input_line.value_suggested_row.id
            value_id = user_input_line.value_suggested.id
            if qid not in answers:
                answers[qid] = {}
            if question.matrix_subtype == 'simple':
                answers[qid][row_id] = value_id
            else:
                if row_id not in answers[qid]:
                    answers[qid][row_id] = []
                answers[qid][row_id].append(value_id)

    def get_answers(self):
        """
        Get all user's answers. Concretely, the survey.user_input_lines are
        grouped by question.

        :return: 2 dictionaries, one containing the answers and the label ids
        (answers) and the other one containing the label values (values).

        - for numerical value questions:
        answers[id] contains the float in value_number
        - for long text zones, text inputs and date/time questions:
        answers[id] contains the string value
        - for multiple choice questions, with only one answer allowed:
        answers[id] contains the id of the survey.label chosen
        - for multiple choice questions, with multiple answers allowed:
        answers[id] contains the list of survey.label ids chosen
        - for matrix questions with one choice per row allowed:
        answers[id] contains a dictionary which keys are the ids of
        survey.label rows and the values are the ids of survey.label answered.
        - for matrix questions with multiple choices per row allowed:
        answers[id] contains a dictionary which keys are the ids of
        survey.label rows and the values are the lists of ids of survey.label
        answered.

        'values' dictionary has the survey.label ids for keys, and the
        survey.label values for values.
        """
        answers = dict()
        values = dict()
        for answer in self.user_input_id.user_input_line_ids:
            self.add_answer(answers, answer)
            labels = answer.value_suggested + answer.value_suggested_row
            for label in labels:
                values[label.id] = label.value
        return answers, values

    def _add_params(self, params):
        """
        Add content in the 'params' dictionary that is accessible during the
        'Python code' field evaluation.
        If you want to give access to special information to your user, simply
        inherit this function.
        """
        answers, values = self.get_answers()
        params['q'] = answers
        params['value'] = values

    @api.one
    def compute_results(self):
        params = {'result': 0.0, 'tag': ''}
        if self.user_input_id and self.computation_id:
            self._add_params(params)
            safe_eval(
                self.computation_id.python_code,
                params,
                mode='exec',
                nocopy=True,
            )
            self.result = float(params['result'])
            self.tag = ustr(params['tag'])

    @api.onchange('computation_id')
    def on_change_computation_id(self):
        self.compute_results()

    @api.onchange('user_input_id')
    def on_change_user_input_id(self):
        self.compute_results()
