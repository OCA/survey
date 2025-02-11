# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    certification_sent = fields.Boolean(
        default=False, help="It indicates if the certification has been sent."
    )

    def _mark_done(self):
        for user_input in self:
            # The response is marked as sent in anticipation that it will be sent safely.
            if (
                user_input.survey_id.certification
                and user_input.scoring_success
                and not user_input.survey_id.skip_certification_email
                and user_input.survey_id.certification_mail_template_id
                and not user_input.test_entry
            ):
                user_input.certification_sent = True
        # Add ids of surveys that have to skip automatic sending to the context
        return super(
            SurveyUserInput,
            self.with_context(
                skip_certification_email_ids=self.mapped("survey_id")
                .filtered(lambda s: s.skip_certification_email)
                .ids
            ),
        )._mark_done()

    def action_manual_send_certification(self):
        # Send certifications manually only to those who passed the survey.
        sent_count = 0
        for user_input in self:
            if (
                user_input.survey_id.certification
                and user_input.scoring_success
                and not user_input.test_entry
            ):
                template = user_input.survey_id.certification_mail_template_id
                if template:
                    template.send_mail(
                        user_input.id, notif_layout="mail.mail_notification_light"
                    )
                    user_input.certification_sent = True
                    sent_count += 1
        if sent_count:
            title = _("Certification Sent")
            message = _("%s certification(s) successfully sent.") % sent_count
            notif_type = "success"
        else:
            title = _("No Certifications Sent")
            message = _("The survey does not meet the conditions.")
            notif_type = "warning"
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "type": notif_type,
                "sticky": False,
            },
        }
