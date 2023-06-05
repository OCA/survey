# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _mark_done(self):
        """Link the generated opportunity and quoation together when the survey
        is submitted."""
        res = super()._mark_done()
        if self.opportunity_id and self.sale_order_id:
            self.opportunity_id.update(
                {
                    "expected_revenue": self.sale_order_id.amount_total,
                    "order_ids": [(6, 0, self.sale_order_id.ids)],
                }
            )
        return res
