import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    record_id = fields.Reference(
        string="Referenced record", selection="_selection_target_model"
    )
    model_id = fields.Many2one("ir.model", related="question_id.model_id")
    answer_values_type = fields.Selection(related="question_id.answer_values_type")
    value_char = fields.Char("Value")

    @api.model
    def _selection_target_model(self):
        return [
            (model.model, model.name)
            for model in self.env["ir.model"].sudo().search([])
        ]

    @api.onchange("record_id")
    def onchange_record_id(self):
        if self.record_id:
            self.value = self.record_id.display_name

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        if not result.get("model_id") or "record_id" not in fields:
            return result

        model = self.env["ir.model"].browse(result.get("model_id")).model
        res = self.env[model].search([], limit=1)
        if res:
            result["record_id"] = "%s,%s" % (
                model,
                res.id,
            )
        return result
