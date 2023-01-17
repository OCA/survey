# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    show_in_lead_description = fields.Boolean()
