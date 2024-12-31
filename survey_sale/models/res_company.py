# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    survey_sale_id = fields.Many2one(
        comodel_name="survey.survey", string="Default Sale Survey"
    )
