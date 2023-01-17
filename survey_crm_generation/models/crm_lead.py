# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    survey_user_input_id = fields.Many2one(comodel_name="survey.user_input")
