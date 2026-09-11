# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _prepare_partner_vals(self, elegible_inputs):
        res = super()._prepare_partner_vals(elegible_inputs)
        for line in elegible_inputs.filtered(lambda x: x.answer_type == "model"):
            field = line.question_id.res_partner_field
            if not field or field.name not in res:
                continue
            if field.ttype == "many2many":
                res[field.name] = [Command.set(line.value_model.ids)]
            else:
                res[field.name] = line.value_model.id
        return res
