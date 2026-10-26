# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    user_metadata = fields.Text(
        help="Metadata gathered during survey validation when legal terms are enabled",
        readonly=True,
    )
