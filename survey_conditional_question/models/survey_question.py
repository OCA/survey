# Copyright 2019 Vuente
# Copyright 2020 Le Filament (<https://www.le-filament.com>)
# License GPL-3.0 or later (https://www.gnu.org/licenses/gpl).

from odoo import api, fields, models


class SurveyQuestionConditional(models.Model):
    _inherit = "survey.question"

    conditional = fields.Boolean(string="Conditional", copy=False)
    conditional_question_id = fields.Many2one(
        comodel_name="survey.question",
        string="Condition Question",
        help="The question which determines if this question is shown",
        copy=False,
    )
    conditional_question_type = fields.Selection(
        related="conditional_question_id.question_type"
    )
    conditional_option_id = fields.Many2one(
        comodel_name="survey.label",
        string="Condition Option",
        help="The option which determines if this question is shown",
        copy=False,
    )
    conditional_minimum_value = fields.Float(
        help="If the value is lower, it will not be shown", copy=False
    )
    conditional_maximum_value = fields.Float(
        help="If the value is higher, it will not be shown", copy=False
    )
    can_be_conditional = fields.Boolean(
        compute="_compute_can_be_conditional", store=True
    )

    def _get_can_be_conditional(self):
        return self.question_type in ["numerical_box", "simple_choice"]

    @api.depends("question_type")
    def _compute_can_be_conditional(self):
        for record in self:
            record.can_be_conditional = record._get_can_be_conditional()

    @api.onchange("constr_mandatory")
    def _onchange_constr_mandatory(self):
        if self.constr_mandatory:
            self.conditional = False
