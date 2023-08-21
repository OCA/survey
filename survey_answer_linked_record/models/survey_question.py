# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    ir_model_id = fields.Many2one(
        string="Model",
        comodel_name="ir.model",
    )
    ir_model_domain = fields.Char(string="Domain")
    ir_model_name = fields.Char(
        string="Model name",
        related="ir_model_id.model",
        readonly=True,
        related_sudo=True,
    )

    def populate_ir_model_suggested_answers(self):
        self.ensure_one()
        # TODO: Maybe add more complex rules. We want to avoid sensible data leaks
        if not self.env.is_admin():
            return
        record_answers = self.env[self.ir_model_id.model].search(
            safe_eval(self.ir_model_domain or [])
        )
        for answer in record_answers:
            self.env["survey.question.answer"].create(
                {
                    "question_id": self.id,
                    "value": answer.display_name,
                    "ir_model_resource_ref": f"{self.ir_model_id.model},{answer.id}",
                }
            )


class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        if not result.get("ir_model_id") or "ir_model_resource_ref" not in fields:
            return result
        model = self.env["ir.model"].browse(result["ir_model_id"])
        res = self.env[model.model].search([], limit=1)
        if res:
            result["ir_model_resource_ref"] = f"{model.model},{res.id}"
        return result

    @api.model
    def _selection_ir_model_resource_ref(self):
        return [(model.model, model.name) for model in self.env["ir.model"].search([])]

    ir_model_id = fields.Many2one(related="question_id.ir_model_id")
    ir_model_resource_ref = fields.Reference(
        string="Model record",
        selection="_selection_ir_model_resource_ref",
    )

    @api.onchange("ir_model_resource_ref")
    def _onchange_ir_model_resource_ref(self):
        """Set the default value as the product name, although we can change it"""
        if self.ir_model_resource_ref:
            self.value = self.ir_model_resource_ref.display_name or ""
