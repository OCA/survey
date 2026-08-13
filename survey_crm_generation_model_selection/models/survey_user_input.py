# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from markupsafe import Markup

from odoo import Command, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _prepare_opportunity(self):
        res = super()._prepare_opportunity()
        for key, value in res.items():
            if isinstance(value, models.BaseModel):
                if len(value) == 1:
                    res[key] = value.id
                else:
                    res[key] = Command.set(value.ids)
        return res

    def _build_answers_html(self, given_answers=False):
        """Extend the basic html answers to render ``model`` answers with the
        referenced record's display name instead of its raw recordset repr,
        keeping the original question order."""

        def _answer_element(title, value):
            return Markup("<li><em>%s</em>: <b>%s</b></li>") % (title, value)

        given_answers = (given_answers or self.user_input_line_ids).filtered(
            lambda x: not x.skipped
        )
        html_parts = []
        for question in given_answers.question_id:
            answer_lines = given_answers.filtered(
                lambda x, q=question: x.question_id == q
            )
            if question.question_type == "model":
                html_parts += [
                    _answer_element(question.title, answer.value_model.display_name)
                    for answer in answer_lines.filtered("value_model")
                ]
            else:
                html_parts.append(
                    super()._build_answers_html(given_answers=answer_lines)
                )
        return Markup("").join(html_parts)
