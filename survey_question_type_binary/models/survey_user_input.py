# Copyright 2023 Jose Zambudio - Aures Tic <jose@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models
from odoo.fields import Command


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        old_answers = self.env["survey.user_input.line"].search(
            [
                ("user_input_id", "=", self.id),
                ("question_id", "=", question.id),
            ]
        )

        if question.question_type in ("binary", "multi_binary"):
            if not isinstance(answer, (list | tuple)):
                answer = [answer]
            if not answer:
                answer = [False]
            for answer_binary in answer:
                old_answers = self._save_line_simple_answer(
                    question, old_answers, answer_binary
                )
        else:
            super()._save_lines(
                question, answer, comment=comment, overwrite_existing=overwrite_existing
            )
        return True

    def _get_line_answer_values(self, question, answer, answer_type):
        vals = super()._get_line_answer_values(question, answer, answer_type)
        if answer_type in ("binary", "multi_binary") and answer:
            if answer_type == "binary":
                del vals["value_binary"]
            else:
                del vals["value_multi_binary"]
            vals.update(
                {
                    "answer_binary_ids": [
                        Command.create(
                            {
                                "value_binary": answer.get("data"),
                                "filename": answer.get("filename"),
                            }
                        )
                    ]
                }
            )
        return vals
