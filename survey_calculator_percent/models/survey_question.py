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

from openerp import api, models


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    @api.one
    @api.depends('type', 'labels_ids', 'labels_ids_2')
    def get_available_answers(self):
        labels = []
        if self.type == 'percent_split':
            for label in self.labels_ids:
                labels.append('[%s] %s' % (label.id, label.value))
            self.available_answers_multiple = '\n'.join(labels)
        else:
            super(SurveyQuestion, self).get_available_answers()

    @api.one
    @api.depends('type', 'matrix_subtype')
    def get_multiple_answers_allowed(self):
        if self.type == 'percent_split':
            self.multiple_answers_allowed = False
        else:
            super(SurveyQuestion, self).get_multiple_answers_allowed()
