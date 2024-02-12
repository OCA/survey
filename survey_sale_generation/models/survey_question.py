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
    # Save into model fields
    allowed_sale_order_field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        compute="_compute_allowed_sale_order_field_ids",
    )
    sale_order_field = fields.Many2one(
        comodel_name="ir.model.fields",
        domain="[('id', 'in', allowed_sale_order_field_ids)]",
    )

    @api.depends("question_type")
    def _compute_allowed_sale_order_field_ids(self):
        type_mapping = {
            "char_box": ["char", "text"],
            "text_box": ["html", "text"],
            "numerical_box": ["integer", "float", "html", "char"],
            "date": ["date", "text", "char"],
            "datetime": ["datetime", "html", "char"],
            "simple_choice": ["html", "char"],
            "multiple_choice": ["html", "char"],
        }
        for record in self:
            record.allowed_sale_order_field_ids = (
                self.env["ir.model.fields"]
                .search(
                    [
                        ("model", "=", "sale.order"),
                        ("ttype", "in", type_mapping.get(record.question_type, [])),
                    ]
                )
                .ids
            )


class SurveyLabel(models.Model):
    _inherit = "survey.question.answer"

    product_ids = fields.Many2many(comodel_name="product.product")

    @api.onchange("product_ids")
    def _onchange_product_ids(self):
        """Set the default value as the product name, although we can change it"""
        if len(self.product_ids) == 1:
            self.value = self.product_ids.name
