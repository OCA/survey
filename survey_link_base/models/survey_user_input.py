# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    res_model = fields.Char()
    res_id = fields.Integer()
