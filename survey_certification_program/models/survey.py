# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
    certification_program_layout = fields.Selection(
        [
            ("simple", "Simple"),
            ("columns", "Columns"),
        ],
        default="simple",
        string="Certificate Layout",
        help="""1. Simple list: The program blocks will be displayed one below the other
in a vertical layout.
2. In columns: The program blocks will be displayed in a table.
""",
    )

    @api.constrains("certification_program_enabled", "certificate_program_line_ids")
    def _check_certification_program_lines_required(self):
        for survey in self:
            if (
                survey.certification_program_enabled
                and not survey.certificate_program_line_ids
            ):
                raise ValidationError(
                    _(
                        "You must add at least one Certification Program Line before saving."
                    )
                )
