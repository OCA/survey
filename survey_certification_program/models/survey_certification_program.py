# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SurveyCertificateProgramLine(models.Model):
    _name = "survey.certificate.program.line"
    _description = "Survey Certificate Program Line"
    _order = "sequence"

    survey_id = fields.Many2one(
        "survey.survey",
        string="Survey",
        help="The survey associated with this certification program line.",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    description = fields.Html()
    hours = fields.Float()
