# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _prepare_partner(self):
        self.ensure_one()
        return {
            line.question_id.res_partner_field.name: line[f"value_{line.answer_type}"]
            for line in self.user_input_line_ids.filtered(
                lambda r: r.question_id.res_partner_field
            )
        }

    def _create_contact_post_process(self):
        """After creating the lead send an internal message with the input link"""
        self.partner_id.message_post_with_view(
            "mail.message_origin_link",
            values={"self": self.partner_id, "origin": self.survey_id},
            subtype_id=self.env.ref("mail.mt_note").id,
        )

    def _mark_done(self):
        """Generate the contact when the survey is submitted"""
        for user_input in self.filtered(
            lambda r: r.survey_id.generate_contact and not self.partner_id
        ):
            vals = user_input._prepare_partner()
            partner = False
            email = vals.get("email")
            if email:
                partner = self.env["res.partner"].search(
                    [("email", "=", email)], limit=1
                )
            if not partner:
                partner = self.env["res.partner"].create(vals)
                self._create_contact_post_process()
            self.write({"partner_id": partner.id, "email": partner.email})
        return super()._mark_done()
