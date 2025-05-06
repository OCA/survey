# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    show_in_lead_description = fields.Boolean()
    # Save into model fields
    allowed_field_domain = fields.Binary(
        compute="_compute_allowed_field_domain",
    )
    crm_lead_field = fields.Many2one(comodel_name="ir.model.fields")

    @api.depends("question_type")
    def _compute_allowed_field_domain(self):
        type_mapping = {
            "char_box": ["char", "text"],
            "text_box": ["html", "text", "char"],
            "numerical_box": ["integer", "float", "html", "char"],
            "date": ["date", "text", "char"],
            "datetime": ["datetime", "html", "char"],
            "simple_choice": ["html", "char"],
            "multiple_choice": ["html", "char"],
        }
        for record in self:
            allowed_types = type_mapping.get(record.question_type, [])
            domain = [
                ("model", "=", "crm.lead"),
                ("ttype", "in", allowed_types),
                ("store", "=", True),
                ("readonly", "=", False),
            ]
            record.allowed_field_domain = domain
