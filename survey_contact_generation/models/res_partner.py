# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    generating_survey_user_input_id = fields.Many2one(
        comodel_name="survey.user_input", copy=False, readonly=True
    )
