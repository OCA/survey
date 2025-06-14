# Copyright 2025 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    certification_company_name = fields.Char(
        "Certification - Company Name",
        help=(
            "Company name to be used in the certification report. "
            "If left blank, the company name will be used."
        ),
        compute="_compute_certification_branding_fields",
        store=True,
        readonly=False,
    )

    certification_logo_512 = fields.Image(
        string="Certification - Logo",
        max_width=512,
        max_height=512,
        help=(
            "Logo to be used in the certification report. "
            "It will be resized to a maximum of 512x512 pixels. "
            "If left blank, the company logo will be used."
        ),
        compute="_compute_certification_branding_fields",
        store=True,
        readonly=False,
    )

    @api.depends("certification")
    def _compute_certification_branding_fields(self):
        """
        Clear the certification branding fields if the survey is not a
        certification
        """
        self.filtered(lambda survey: not survey.certification).update(
            {
                "certification_company_name": False,
                "certification_logo_512": False,
            }
        )
