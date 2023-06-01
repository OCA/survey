# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    allowed_field_ids = fields.Many2many(
        comodel_name="ir.model.fields", compute="_compute_allowed_field_ids",
    )
    res_partner_field = fields.Many2one(
        string="Contact field",
        comodel_name="ir.model.fields",
        domain="[('id', 'in', allowed_field_ids)]",
    )

    @api.depends("question_type")
    def _compute_allowed_field_ids(self):
        type_mapping = {
            "textbox": ["char"],
            "free_text": ["text"],
            "numerical_box": ["integer", "float"],
            "date": ["date"],
            "datetime": ["datetime"],
        }
        for record in self:
            record.allowed_field_ids = (
                self.env["ir.model.fields"]
                .search(
                    [
                        ("model", "=", "res.partner"),
                        ("ttype", "in", type_mapping.get(record.question_type, [])),
                    ]
                )
                .ids
            )
