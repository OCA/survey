# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    show_in_lead_description = fields.Boolean()
    # Save into model fields
    allowed_crm_lead_field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        compute="_compute_allowed_crm_lead_field_ids",
    )
    crm_lead_field = fields.Many2one(
        comodel_name="ir.model.fields",
        domain="[('id', 'in', allowed_crm_lead_field_ids)]",
    )

    @api.depends("question_type")
    def _compute_allowed_crm_lead_field_ids(self):
        type_mapping = {
            "char_box": ["char", "text"],
            "text_box": ["html", "text"],
            "numerical_box": ["integer", "float", "html", "char"],
            "date": ["date", "text", "char"],
            "datetime": ["datetime", "html", "char"],
            "simple_choice": ["html", "char"],
            "multiple_choice": ["html", "char"],
        }
        for record in self:
            record.allowed_crm_lead_field_ids = (
                self.env["ir.model.fields"]
                .search(
                    [
                        ("model", "=", "crm.lead"),
                        ("ttype", "in", type_mapping.get(record.question_type, [])),
                    ]
                )
                .ids
            )
