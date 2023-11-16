# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    send_result_mail = fields.Boolean(
        string="Send survey answers",
        help="When the survey is submitted, an email will be sent to the user with"
        "the answers",
    )
    result_mail_template_id = fields.Many2one(
        comodel_name="mail.template", domain="[('model', '=', 'survey.user_input')]"
    )
