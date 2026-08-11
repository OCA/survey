# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    skip_start = fields.Boolean(
        string="Skip start screen",
        help="Skip the start screen and go directly to the survey form",
    )

    def _create_answer(self, *args, **additional_vals):
        """The survey template checks the state of the inputs to show the start screen
        or not. Setting the state we go directly to the form"""
        inputs = super()._create_answer(*args, **additional_vals)
        inputs.filtered(
            lambda input: input.survey_id.skip_start and not input.is_session_answer
        ).state = "in_progress"
        return inputs
