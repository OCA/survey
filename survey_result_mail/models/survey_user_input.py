# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from markupsafe import Markup

from odoo import fields, models
from odoo.tools import format_date, format_datetime, is_html_empty


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    survey_result = fields.Html(compute="_compute_survey_result")

    def _compute_survey_result(self):
        mode = self.env.context.get("survey_result_mode", "basic")
        for user_input in self:
            if mode == "bootstrap":
                user_input.survey_result = user_input._render_user_input()
            elif mode == "basic":
                user_input.survey_result = user_input._build_answers_html()

    def _render_user_input(self):
        """We're rendering the template results to add them to the pdf report"""
        self.ensure_one()
        survey_sudo = self.survey_id.sudo()
        answer_sudo = self.sudo()
        return (
            self.env["ir.ui.view"]
            .sudo()
            ._render_template(
                "survey_result_mail.survey_page_print",
                {
                    "is_html_empty": is_html_empty,
                    "review": False,
                    "survey": survey_sudo,
                    "answer": answer_sudo,
                    "questions_to_display": answer_sudo._get_print_questions(),
                    "scoring_display_correction": (
                        survey_sudo.scoring_type == "scoring_with_answers"
                        and answer_sudo
                    ),
                    "format_datetime": lambda dt: format_datetime(
                        self.env, dt, dt_format=False
                    ),
                    "format_date": lambda date: format_date(self.env, date),
                },
            )
        )

    def _build_answers_html(self, given_answers=False):
        """Basic html formatted answers. Can be used in mail communications and other
        html fields without worring about styles"""

        def _answer_element(title, value):
            return f"<li><em>{title}</em>: <b>{value}</b></li>"

        given_answers = (given_answers or self.user_input_line_ids).filtered(
            lambda x: not x.skipped
        )
        questions_dict = {}
        for answer in given_answers.filtered(lambda x: x.answer_type != "suggestion"):
            questions_dict[answer.question_id] = _answer_element(
                answer.question_id.title, answer[f"value_{answer.answer_type}"]
            )
        for answer in given_answers.filtered(
            lambda x: x.question_id.question_type == "simple_choice"
        ):
            questions_dict[answer.question_id] = _answer_element(
                answer.question_id.title,
                answer.suggested_answer_id.value or answer.value_char_box,
            )
        multiple_choice_dict = {}
        for answer in given_answers.filtered(
            lambda x: x.question_id.question_type == "multiple_choice"
        ):
            multiple_choice_dict.setdefault(answer.question_id, [])
            multiple_choice_dict[answer.question_id].append(
                answer.suggested_answer_id.value or answer.value_char_box
            )
        for question, answers in multiple_choice_dict.items():
            questions_dict[question] = _answer_element(
                question.title, " / ".join([x for x in answers if x])
            )
        matrix_dict = {}
        for answer in given_answers.filtered(
            lambda x: x.question_id.question_type == "matrix"
        ):
            matrix_dict.setdefault(answer.question_id, {})
            matrix_dict[answer.question_id].setdefault(answer.matrix_row_id, [])
            matrix_dict[answer.question_id][answer.matrix_row_id].append(
                answer.suggested_answer_id.value or answer.value_char_box
            )
        for question, rows in matrix_dict.items():
            questions_dict[question] = f"<li><em>{question.title}:</em><ul>"
            for row, answers in rows.items():
                questions_dict[question] += _answer_element(
                    row.value, " / ".join([x for x in answers if x])
                )
            questions_dict[question] += "</ul></li>"
        answers_html = "".join([questions_dict[q] for q in given_answers.question_id])
        return Markup(answers_html)

    def _mark_done(self):
        """Send the answers when submitted on the so configured surveys"""
        res = super()._mark_done()
        for user_input in self.filtered(
            lambda x: x.survey_id.send_result_mail and x.partner_id.email or x.email
        ):
            template = self.survey_id.result_mail_template_id or self.env.ref(
                "survey_result_mail.mail_template_user_input_result_inline"
            )
            template.send_mail(
                user_input.id, notif_layout="mail.mail_notification_light"
            )
        return res
