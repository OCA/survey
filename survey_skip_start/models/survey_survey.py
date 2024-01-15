# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    skip_start = fields.Boolean(
        string="Skip start screen",
        help="Skip the start screen and go directly to the survey form",
    )

    @api.constrains("skip_start")
    def _constrain_skip_start(self):
        """For the moment, skipping the start screen is only compatible with single
        page layout surveys"""
        if self.filtered(lambda x: x.skip_start and x.questions_layout != "one_page"):
            raise UserError(
                _(
                    "The skip start screen option is only compatible with on page layouts"
                )
            )
