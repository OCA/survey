# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    opportunity_id = fields.Many2one(comodel_name="crm.lead")

    def _prepare_opportunity(self):
        vals = {
            "name": self.survey_id.title,
            "tag_ids": [(6, 0, self.survey_id.crm_tag_ids.ids)],
            "partner_id": self.partner_id.id,
            "user_id": self.survey_id.crm_team_id.user_id.id,
            "team_id": self.survey_id.crm_team_id.id,
            "company_id": self.create_uid.company_id.id,
            "survey_user_input_id": self.id,
            "description": self._prepare_lead_description(),
        }
        if not self.partner_id:
            vals.update(
                {
                    "email_from": self.email,
                    "contact_name": self.nickname,
                }
            )
        # Fill sale.order fields from answers
        elegible_inputs = self.user_input_line_ids.filtered(
            lambda x: x.question_id.crm_lead_field and not x.skipped
        )
        basic_inputs = elegible_inputs.filtered(
            lambda x: x.answer_type not in {"suggestion"}
        )
        vals.update(
            {
                line.question_id.crm_lead_field.name: line[f"value_{line.answer_type}"]
                for line in basic_inputs
            }
        )
        for line in elegible_inputs - basic_inputs:
            field_name = line.question_id.crm_lead_field.name
            value = (
                line.suggested_answer_id.value
                if line.answer_type == "suggestion"
                else line[f"value_{line.answer_type}"]
            )
            vals[field_name] = value
        return vals

    def _prepare_lead_description(self):
        """We can have surveys without partner. It's handy to have some relevant info
        in the description although the answers are linked themselves.

        :return str: description for the lead
        """
        return self._build_answers_html(
            self.user_input_line_ids.filtered("question_id.show_in_lead_description")
        )

    def _create_opportunity_post_process(self):
        """After creating the lead send an internal message with the input link"""
        self.opportunity_id.message_post_with_view(
            "mail.message_origin_link",
            values={"self": self.opportunity_id, "origin": self.survey_id},
            subtype_id=self.env.ref("mail.mt_note").id,
        )

    def _mark_done(self):
        """Generate the opportunity when the survey is submitted"""
        res = super()._mark_done()
        if not self.survey_id.generate_leads:
            return res
        vals = self._prepare_opportunity()
        self.opportunity_id = self.env["crm.lead"].sudo().create(vals)
        self._create_opportunity_post_process()
        return res
