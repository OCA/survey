# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class Survey(models.Model):
    _inherit = "survey.survey"

    skip_certification_email = fields.Boolean(
        help="Skip sending the certification automatically after successful completion "
        "of the survey."
    )
