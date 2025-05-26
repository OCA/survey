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
            survey_input = self.env["survey.user_input"].browse(res_id)
            if (
                survey_input.survey_id.skip_certification_email
                or survey_input.partner_id.skip_certification_email
            ):
                return False
        return super().send_mail(
            res_id, force_send, raise_exception, email_values, notif_layout
        )
