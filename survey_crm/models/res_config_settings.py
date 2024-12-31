# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty
# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    survey_crm_id = fields.Many2one(
        comodel_name="survey.survey",
        string="Default CRM Survey",
        related="company_id.survey_crm_id",
        readonly=False,
    )
