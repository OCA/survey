# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    crm_team_id = fields.Many2one(comodel_name="crm.team")
    generate_quotations = fields.Boolean(
        help="Check it to generate sale orders from the survey answers. You'll need to "
        "configure at least one question linked to a product."
    )
    send_quotation_to_customer = fields.Boolean(
        help="Send the quotation to the customer automatically."
    )
    quotation_mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        domain=[("model", "=", "sale.order")],
        help="Choose a template. Otherwise the default one will be used.",
    )
    sale_order_template_id = fields.Many2one(
        comodel_name="sale.order.template",
    )
