# Copyright 2019 Vuente
# Copyright 2020 Le Filament (<https://www.le-filament.com>)
# License GPL-3.0 or later (https://www.gnu.org/licenses/gpl).

from odoo import api, fields, models


class SurveyQuestionConditional(models.Model):
    _inherit = "survey.question"

    conditional = fields.Boolean(string="Conditional")
    conditional_question_id = fields.Many2one(
        comodel_name='survey.question',
        string="Condition Question",
        help="The question which determines if this question is shown")
    conditional_option_id = fields.Many2one(
        comodel_name='survey.label',
        string="Condition Option",
        help="The option which determines if this question is shown")

    @api.onchange('constr_mandatory')
    def _onchange_constr_mandatory(self):
        if self.constr_mandatory:
            self.conditional = False
