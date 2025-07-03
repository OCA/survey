# Copyright 2025 Binhex - Zuzanna Elżbieta Szalaty Szalaty
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_type = fields.Selection(selection_add=[("signature", _("Signature"))])
