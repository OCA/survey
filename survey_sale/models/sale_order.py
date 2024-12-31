# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "survey.link.mixin"]

    def get_default_survey(self):
        res = super().get_default_survey()
        if self.env.company.survey_sale_id:
            return self.env.company.survey_sale_id.id
        return res
