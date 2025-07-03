# Copyright 2025 Binhex - Zuzanna Elżbieta Szalaty Szalaty
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def save_lines(self, question, answer, comment=None):
        self.ensure_one()
        old_answers = self.env["survey.user_input.line"].search(
            [("user_input_id", "=", self.id), ("question_id", "=", question.id)]
        )
        if question.question_type in ["signature"]:
            self._save_line_signature(question, old_answers, answer)
        else:
            return super().save_lines(question, answer, comment)

    def _save_line_signature(self, question, old_answers, answer):
        vals = self._get_line_answer_values(question, answer, question.question_type)
        if old_answers:
            old_answers.write(vals)
            return old_answers
        return self.env["survey.user_input.line"].create(vals)
