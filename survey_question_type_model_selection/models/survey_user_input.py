# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        old_answers = self.env["survey.user_input.line"].search(
            [
                ("user_input_id", "=", self.id),
                ("question_id", "=", question.id),
            ]
        )
        if question.question_type == "model":
            if not answer:
                answer = False
            else:
                answer = f"{question.question_model_id.model},{answer}"
            self._save_line_simple_answer(question, old_answers, answer)
        else:
            super()._save_lines(
                question, answer, comment=comment, overwrite_existing=overwrite_existing
            )
        return True

    def _get_line_answer_values(self, question, answer, answer_type):
        res = super()._get_line_answer_values(question, answer, answer_type)
        if answer_type == "model":
            res["value_model"] = answer
        return res
