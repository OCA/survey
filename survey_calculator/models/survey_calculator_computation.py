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


class SurveyCalculatorComputation(models.Model):
    _name = 'survey.calculator.computation'
    _description = "Survey Calculator Computation"

    @api.depends('survey_id')
    def get_questions_available(self):
        self.question_ids = self.mapped('survey_id.page_ids.question_ids')

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )
    survey_id = fields.Many2one(
        comodel_name='survey.survey',
        string='Survey',
        required=True,
        help='The survey on which the calculation will be done.'
    )
    python_code = fields.Text(
        string='Python Code',
        help='Python code that will allow to do calculations with the survey '
             'answers.',
    )
    question_ids = fields.Many2many(
        comodel_name='survey.question',
        string='Available Answers',
        copy=True,
        readonly=True,
        help='Available Answers that can be used in the calculation.',
        compute='get_questions_available',
    )
    display_help_text = fields.Boolean(
        'Display help text?',
        default=True,
    )
    calculator_result_ids = fields.One2many(
        comodel_name='survey.calculator.result',
        inverse_name='computation_id'
    )

    @api.multi
    def compute_all_inputs(self):
        """
        Do the computation for all user inputs associated to the survey.
        """
        for user_input in self.survey_id.user_input_ids:
            results = user_input.calculator_result_ids
            already_computed = self in results.mapped('computation_id')
            if user_input.state == 'done' and not already_computed:
                result_pool = self.env['survey.calculator.result']
                result_pool.create({
                    'computation_id': self.id,
                    'user_input_id': user_input.id,
                })
