# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    answer_type = fields.Selection(
        selection_add=[
            ("model", "Model selection"),
        ]
    )
    value_model = fields.Reference(
        string="Selection answer", selection="_selection_target_model"
    )

    def _compute_display_name(self):
        for line in self:
            if line.answer_type == "model":
                line.display_name = line.value_model.display_name
        return super()._compute_display_name()

    @api.model
    def _selection_target_model(self):
        return [
            (model.model, model.name)
            for model in self.env["ir.model"].sudo().search([])
        ]
