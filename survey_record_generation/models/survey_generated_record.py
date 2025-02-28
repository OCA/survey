# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyGeneratedRecord(models.Model):
    _name = "survey.generated.record"

    survey_record_creation_name = fields.Char("Name", readonly=True)
    survey_record_creation_id = fields.Many2one(
        "survey.record.creation", "Survey record creation", readonly=True
    )
    user_input_id = fields.Many2one("survey.user_input", "Participation", readonly=True)
    created_record_id = fields.Reference(
        string="Referenced record", selection="_selection_target_model", readonly=True
    )

    @api.model
    def _selection_target_model(self):
        return [
            (model.model, model.name)
            for model in self.env["ir.model"].sudo().search([])
        ]
