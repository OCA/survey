# Copyright Odoo
# Copyright 2025 Kencove - Mohamed Alkobrosli (http://kencove.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

import werkzeug

from odoo import _, models, tools
from odoo.exceptions import UserError

emails_split = re.compile(r"[;,\n\r]+")


class take_survey_wizard(models.TransientModel):
    _inherit = "survey.invite"

    def action_invite_base(self):
        """Process the wizard content and proceed with sending the related
        email(s), rendering any template patterns on the fly if needed"""
        self.ensure_one()
        Partner = self.env["res.partner"]
        # compute partners and emails, try to find partners for given emails
        valid_partners = self.partner_ids
        langs = set(valid_partners.mapped("lang")) - {False}
        if len(langs) == 1:
            self = self.with_context(lang=langs.pop())
        valid_emails = []
        for email in emails_split.split(self.emails or ""):
            partner = False
            email_normalized = tools.email_normalize(email)
            if email_normalized:
                limit = None if self.survey_users_login_required else 1
                partner = Partner.search(
                    [("email_normalized", "=", email_normalized)], limit=limit
                )
            if partner:
                valid_partners |= partner
            else:
                email_formatted = tools.email_split_and_format(email)
                if email_formatted:
                    valid_emails.extend(email_formatted)
        if not valid_partners and not valid_emails:
            raise UserError(_("Please enter at least one valid recipient."))
        answers = self._prepare_answers(valid_partners, valid_emails)
        send_method = self.env.context.get("send_method", "")
        if send_method == "email":
            for answer in answers:
                self._send_mail(answer)
        elif send_method == "sms":
            for answer in answers:
                self.send_sms(answer)
        else:
            for answer in answers:
                self._send_mail(answer)
                self.send_sms(answer)

    def send_sms(self, answer):
        survey_start_url = self._get_survey_start_url(answer)
        body = self._render_field("body", answer.ids, post_process=True)[answer.id]
        body_html = self.env["mail.render.mixin"]._replace_local_links(body)
        message = self.env["ir.fields.converter"].text_from_html(body_html)
        for number in filter(None, [answer.partner_id.phone, answer.partner_id.mobile]):
            self._send_sms(
                message,
                survey_start_url,
                answer.partner_id,
                self.create_uid.name,
                number,
            )

    def _send_sms(self, message, link, partner, requested_by_user, partner_phone_field):
        message = self.env["ir.fields.converter"].text_from_html(message)
        template = self.env.ref(
            "partner_survey_sms.partner_survey_sms_template_notification"
        ).with_context(
            **{
                "requested_by_user": requested_by_user,
                "message": message,
                "link": link,
            }
        )
        body = template._render_field("body", partner.ids, compute_lang=True)[
            partner.id
        ]
        composer = (
            self.env["sms.composer"]
            .with_context(
                default_composition_mode="comment",
                default_res_id=partner.id,
                default_res_model="res.partner",
                default_template_id=False,
            )
            .create(
                {
                    "body": body,
                    "number_field_name": partner_phone_field,
                }
            )
        )
        composer.action_send_sms()

    def _get_survey_start_url(self, answer):
        survey_start_url = (
            werkzeug.urls.url_join(self.get_base_url(), answer.get_start_url())
            if answer
            else False
        )
        return survey_start_url
