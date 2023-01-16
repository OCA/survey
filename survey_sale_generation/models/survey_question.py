# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    product_id = fields.Many2one(comodel_name="product.product")
    show_in_sale_order_comment = fields.Boolean()


class SurveyLabel(models.Model):
    _inherit = "survey.label"

    product_id = fields.Many2one(comodel_name="product.product")

    @api.onchange("product_id")
    def _onchange_product_id(self):
        """Set the default value as the product name, although we can change it"""
        self.value = self.product_id.display_name or ""
