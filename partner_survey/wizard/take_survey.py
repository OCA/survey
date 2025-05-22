# Copyright 2025 Kencove - Mohamed Alkobrosli
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class take_survey_wizard(models.TransientModel):
    """Wizard allowing to take a survey from partners form view"""

    _name = "res.partner.survey.survey.wizard"

    partner_ids = fields.Many2many("res.partner", required=True)
    survey_id = fields.Many2one("survey.survey", required=True)
    state_id = fields.Many2one(
        "res.country.state",
        string="State",
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        partner_ids = self.env.context.get("default_partner_ids")
        state_id = self.env["res.partner"].browse(partner_ids).state_id
        if state_id:
            res["state_id"] = state_id
        return res

    def action_take_survey(self):
        email_template = self.env["mail.template"]
        domain = [
            ("survey_id", "=", self.survey_id.id),
            "|",
            ("state_ids", "in", self.state_id.ids),
            ("state_ids", "=", False),
        ]
        default_template_1 = email_template.search(domain)
        default_template_2 = email_template.get_default_template()
        default_template = default_template_1 or default_template_2
        local_context = dict(
            self.env.context,
            default_use_template=bool(default_template),
            default_template_id=default_template.id or False,
            default_email_layout_xmlid="mail.mail_notification_light",
            default_survey_id=self.survey_id.id,
            default_partner_ids=self.partner_ids.ids,
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Share a Survey"),
            "view_mode": "form",
            "res_model": "survey.invite",
            "target": "new",
            "context": local_context,
        }
