# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    certification_program_enabled = fields.Boolean(
        string="Certification Program",
        help="Allows you to enable program lines",
    )
    certificate_program_line_ids = fields.One2many(
        "survey.certificate.program.line",
        "survey_id",
        string="Certification Program Lines",
        help="The certification program lines associated with this survey.",
    )
    certificate_program_layout = fields.Selection(
        [
            ("simple", "Simple"),
            ("columns", "Columns"),
        ],
        string="Certificate Layout",
        help="""1. Simple list: The program blocks will be displayed one below the other
in a vertical layout.
2. In columns: The program blocks will be displayed in a table.
""",
    )
