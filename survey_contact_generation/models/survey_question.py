# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    allowed_partner_field_domain = fields.Binary(
        compute="_compute_allowed_partner_field_domain",
    )
    res_partner_field = fields.Many2one(
        string="Contact field",
        comodel_name="ir.model.fields",
    )

    @api.depends("question_type")
    def _compute_allowed_partner_field_domain(self):
        type_mapping = {
            "char_box": ["char", "text"],
            "text_box": ["html"],
            "numerical_box": ["integer", "float", "html", "char"],
            "date": ["date", "text", "char"],
            "datetime": ["datetime", "html", "char"],
            "simple_choice": ["many2one", "html", "char"],
            "multiple_choice": ["many2many", "html", "char"],
        }
        for record in self:
            allowed_types = type_mapping.get(record.question_type, [])
            domain = [
                ("model", "=", "res.partner"),
                ("ttype", "in", allowed_types),
                ("store", "=", True),
                ("readonly", "=", False),
            ]
            record.allowed_partner_field_domain = domain


class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        if (
            not result.get("res_partner_field")
            or "res_partner_field_resource_ref" not in fields
        ):
            return result
        partner_field = self.env["ir.model.fields"].browse(result["res_partner_field"])
        # Otherwise we'll just use the value (char, text)
        if partner_field.ttype not in {"many2one", "many2many"}:
            return result
        res = self.env[partner_field.relation].search([], limit=1)
        if res:
            result[
                "res_partner_field_resource_ref"
            ] = f"{partner_field.relation},{res.id}"
        return result

    @api.model
    def _selection_res_partner_field_resource_ref(self):
        return [(model.model, model.name) for model in self.env["ir.model"].search([])]

    res_partner_field = fields.Many2one(related="question_id.res_partner_field")
    res_partner_field_resource_ref = fields.Reference(
        string="Contact field value",
        selection="_selection_res_partner_field_resource_ref",
    )

    @api.onchange("res_partner_field_resource_ref")
    def _onchange_res_partner_field_resource_ref(self):
        """Set the default value as the product name, although we can change it"""
        if self.res_partner_field_resource_ref:
            self.value = self.res_partner_field_resource_ref.display_name or ""
