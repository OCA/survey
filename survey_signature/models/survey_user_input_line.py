# Copyright 2025 Binhex - Zuzanna Elżbieta Szalaty Szalaty
# Copyright 2025 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    value_signature = fields.Binary("Signature")
    answer_type = fields.Selection(selection_add=[("signature", _("Signature"))])

    @api.depends("answer_type")
    def _compute_display_name(self):
        for line in self:
            if line.answer_type == "signature":
                line.display_name = (
                    _("Signed") if line.value_signature else _("Not Signed")
                )
        return super()._compute_display_name()
