# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models
from odoo.tools import format_date, format_datetime


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    survey_result = fields.Html(compute="_compute_survey_result")

    def _render_user_input(self):
        """We're rendering the template results to add them to the pdf report. This
        should be easier in v15"""
        self.ensure_one()
        return (
            self.env["ir.ui.view"]
            .sudo()
            .render_template(
                "survey_result_mail.survey_page_print",
                {
                    "review": True,
                    "survey": self.survey_id,
                    "answer": self,
                    "questions_to_display": self.survey_id.question_ids,
                    "scoring_display_correction": (
                        self.scoring_type == "scoring_with_answers" and self
                    ),
                    "format_datetime": lambda dt: format_datetime(
                        self.env, dt, dt_format=False
                    ),
                    "format_date": lambda date: format_date(self.env, date),
                },
            )
        )

    def _compute_survey_result(self):
        for user_input in self:
            user_input.survey_result = user_input._render_user_input()

    def _mark_done(self):
        """Send the answers when submitted on the so configured surveys"""
        res = super()._mark_done()
        for user_input in self.filtered(
            lambda x: x.survey_id.send_result_mail and x.partner_id.email
        ):
            self.env.ref(
                "survey_result_mail.mail_template_user_input_result"
            ).send_mail(user_input.id, notif_layout="mail.mail_notification_light")
        return res
