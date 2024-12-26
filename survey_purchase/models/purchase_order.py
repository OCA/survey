# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = ["purchase.order", "survey.link.mixin"]

    def get_default_survey(self):
        res = super().get_default_survey()
        if self.env.company.survey_purchase_id:
            return self.env.company.survey_purchase_id.id
        return res
