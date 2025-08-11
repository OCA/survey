# Copyright 2025 Grupo Isonor - Alexandre D. Díaz
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from markupsafe import Markup

from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _build_answers_html(self, given_answers=False):
        def _answer_element_binary(title, value):
            return f"<li><em>{title}</em>: <b>{value}</b></li>"

        def _answer_element_multi_binary(value):
            return f"<li><b>{value}</b></li>"

        given_answers = (given_answers or self.user_input_line_ids).filtered(
            lambda x: not x.skipped
        )
        answers_bin = given_answers.filtered(
            lambda x: x.answer_type in ("binary", "multi_binary")
        )
        given_answers_without_bin = given_answers - answers_bin
        if not given_answers_without_bin:
            # FIXME: This is necessary because we do not want “super” to take
            # into account records of type ‘binary’ or “multi_binary”.
            res_markdown = Markup("")
        else:
            res_markdown = super()._build_answers_html(given_answers_without_bin)

        questions_dict = {}
        for answer in answers_bin:
            if answer.answer_type == "binary":
                questions_dict[answer.question_id] = _answer_element_binary(
                    answer.question_id.title, answer.answer_binary_ids[0].filename
                )
            else:
                questions_dict[
                    answer.question_id
                ] = f"<li><em>{answer.question_id.title}: </em><ul>"
                for bin_id in answer.answer_binary_ids:
                    questions_dict[answer.question_id] += _answer_element_multi_binary(
                        bin_id.filename
                    )
                questions_dict[answer.question_id] += "</ul></li>"
        answers_html = "".join([questions_dict[q] for q in answers_bin.question_id])
        return res_markdown + answers_html

    def _mark_done(self):
        user_input_proc = []
        attachments = {}
        for user_input in self:
            bin_answers = user_input.user_input_line_ids.filtered(
                lambda x: not x.skipped and x.answer_type in ("binary", "multi_binary")
            )
            attachments[user_input.id] = []
            for answer in bin_answers:
                for bin_id in answer.answer_binary_ids:
                    attachments[user_input.id].append(
                        (bin_id.filename, bin_id.value_binary)
                    )
            if not attachments[user_input.id]:
                continue

            if user_input.survey_id.send_result_mail and (
                user_input.partner_id.email or user_input.email
            ):
                user_input.survey_id.update({"send_result_mail": False})
                user_input_proc.append(user_input)

        try:
            res = super()._mark_done()
        finally:
            for user_input in user_input_proc:
                user_input.survey_id.update({"send_result_mail": True})

        for user_input in user_input_proc:
            template = user_input.survey_id.result_mail_template_id or self.env.ref(
                "survey_result_mail.mail_template_user_input_result_inline"
            )
            template.send_mail(
                user_input.id,
                notif_layout="mail.mail_notification_light",
                email_values={
                    "attachments": attachments[user_input.id],
                },
            )

        return res
