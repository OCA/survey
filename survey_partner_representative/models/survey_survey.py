# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    allow_partner_representing = fields.Boolean(
        help="A user with the proper permissions, could do the survey on "
        "behalf of other"
    )

    def _create_answer(self, *args, **kwargs):
        # Inject the context so the partner representation is only done on a normal
        # survey workflow
        if self.allow_partner_representing:
            self = self.with_context(survey_partner_representative=True)
        return super()._create_answer(*args, **kwargs)
