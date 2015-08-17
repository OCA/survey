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


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    @api.one
    @api.depends('type', 'labels_ids', 'labels_ids_2')
    def get_available_answers(self):
        labels = []
        types = []
        rows = []
        if self.type in ['simple_choice', 'multiple_choice']:
            for label in self.labels_ids:
                labels.append('[%s] %s' % (label.id, label.value))
            self.available_answers_multiple = '\n'.join(labels)
        elif self.type == 'matrix':
            for type in self.labels_ids:
                types.append('[%s] %s' % (type.id, type.value))
            self.available_answers_matrix_type = '\n'.join(types)
            for row in self.labels_ids_2:
                rows.append('[%s] %s' % (row.id, row.value))
            self.available_answers_matrix_row = '\n'.join(rows)

    @api.one
    @api.depends('type', 'matrix_subtype')
    def get_multiple_answers_allowed(self):
        self.multiple_answers_allowed = (self.type == 'multiple_choice') or \
            (self.type == 'matrix' and self.matrix_subtype == 'multiple')

    multiple_answers_allowed = fields.Boolean(
        'Multiple answers allowed',
        readonly=True,
        help='Are multiple answers allowed ?',
        compute='get_multiple_answers_allowed',
    )

    available_answers_multiple = fields.Char(
        'Available answers for multiple choices questions',
        readonly=True,
        help="Display a simplified list of the available answers",
        compute='get_available_answers',
    )

    available_answers_matrix_type = fields.Char(
        'Type of answers available for matrix questions',
        readonly=True,
        help="Display a simplified list of the available type of answers",
        compute='get_available_answers',
    )

    available_answers_matrix_row = fields.Char(
        'Rows available for matrix questions',
        readonly=True,
        help="Display a simplified list of the available rows",
        compute='get_available_answers',
    )

    @api.onchange('labels_ids', 'labels_ids_2')
    def on_change_answers(self):
        self.get_available_answers()
