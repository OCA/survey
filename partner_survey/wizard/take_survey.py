from odoo import _, fields, models


class take_survey_wizard(models.TransientModel):
    """Wizard allowing to take a survey from partners form view"""

    _name = "res.partner.survey.survey.wizard"

    partner_ids = fields.Many2many("res.partner", required=True)
    survey_id = fields.Many2one("survey.survey", required=True)

    def action_take_survey(self):
        local_context = dict(
            self.env.context,
            default_use_template=False,
            default_template_id=False,
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
