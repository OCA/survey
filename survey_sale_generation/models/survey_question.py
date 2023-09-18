# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    product_ids = fields.Many2many(comodel_name="product.product")
    product_uom_qty_question_id = fields.Many2one(
        comodel_name="survey.question",
        help="For multiple answer questions we might want to consider how much of that "
        "product we want to order. For example, one question could be: 'How many "
        "members in your team?' and other could be 'Choose the membership type'. We'll "
        "want to multiply members by memberships in our sale line.",
    )
    show_in_sale_order_comment = fields.Boolean()


class SurveyLabel(models.Model):
    _inherit = "survey.question.answer"

    product_ids = fields.Many2many(comodel_name="product.product")

    @api.onchange("product_ids")
    def _onchange_product_ids(self):
        """Set the default value as the product name, although we can change it"""
        if len(self.product_ids) == 1:
            self.value = self.product_ids.name
