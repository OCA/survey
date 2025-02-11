# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    def send_mail(
        self,
        res_id,
        force_send=False,
        raise_exception=False,
        email_values=None,
        notif_layout=False,
    ):
        if self.model == "survey.user_input":
            skip_ids = self.env.context.get("skip_certification_email_ids", [])
            survey = self.env["survey.user_input"].browse(res_id).survey_id
            if survey.id in skip_ids:
                return False
        return super().send_mail(
            res_id, force_send, raise_exception, email_values, notif_layout
        )
