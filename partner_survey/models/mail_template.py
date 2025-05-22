# Copyright 2025 Kencove - Mohamed Alkobrosli
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    set_default_for_share = fields.Boolean()
    model_name = fields.Char(related="model_id.model")
    survey_id = fields.Many2one("survey.survey")
    state_ids = fields.Many2many(
        "res.country.state",
        string="State",
    )

    def write(self, vals):
        if vals.get("set_default_for_share"):
            self._unset_default_on_others()
        return super().write(vals)

    def get_default_template(self):
        return self.search([("set_default_for_share", "=", True)])[:1]

    def _unset_default_on_others(self):
        """Unset set_default_for_share on all other records"""
        default_template = self.get_default_template()
        if default_template:
            default_template.write({"set_default_for_share": False})

    @api.onchange("model_id")
    def _onchange_model_id(self):
        for rec in self:
            if rec.model_id.model != "survey.user_input":
                rec.set_default_for_share = False
