# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _prepare_partner_vals(self, elegible_inputs):
        res = super()._prepare_partner_vals(elegible_inputs)
        for key, value in res.items():
            if isinstance(value, models.BaseModel):
                if len(value) == 1:
                    res[key] = value.id
                else:
                    res[key] = [Command.set(value.ids)]
        return res
