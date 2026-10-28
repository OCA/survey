# Copyright 2026 Acsone
# @author Pierre Verkest <pierre.verkest@apycod.fr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    state = fields.Selection(tracking=True)

    def action_reopen_for_edition(self):
        self.ensure_one()
        self.write(
            {
                "state": "in_progress",
                "last_displayed_page_id": False,
                "survey_first_submitted": False,
            }
        )

    def _save_lines(self, question, answer, comment=None, overwrite_existing=False):
        if self.survey_id.allow_editing:
            overwrite_existing = True
        return super()._save_lines(
            question, answer, comment=comment, overwrite_existing=overwrite_existing
        )
