# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """Set won the linked opportunities automatically"""
        res = super().action_confirm()
        self.filtered(
            lambda x: x.survey_user_input_id and x.opportunity_id
        ).opportunity_id.action_set_won()
        return res
