# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    opportunity_id = fields.Many2one(comodel_name="crm.lead")

    def _prepare_opportunity(self):
        return {
            "name": self.survey_id.title,
            "tag_ids": [(6, 0, self.survey_id.crm_tag_ids.ids)],
            "partner_id": self.partner_id.id,
            "user_id": self.survey_id.crm_team_id.user_id.id,
            "team_id": self.survey_id.crm_team_id.id,
            "company_id": self.create_uid.company_id.id,
            "survey_user_input_id": self.id,
            "description": self._prepare_lead_description(),
        }

    def _prepare_lead_description(self):
        """We can have surveys without partner. It's handy to have some relevant info
        in the description although the answers are linked themselves.

        :return str: description for the lead
        """
        relevant_answers = self.user_input_line_ids.filtered(
            lambda x: not x.skipped and x.question_id.show_in_lead_description
        )
        description = "\n".join(
            f"{answer.question_id.title}: {answer[f'value_{answer.answer_type}']}"
            for answer in relevant_answers
        )
        return description

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
