# Copyright 2023 Jose Zambudio - Aures Tic <jose@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def save_lines(self, question, answer, comment=None):
        old_answers = self.env["survey.user_input.line"].search(
            [
                ("user_input_id", "=", self.id),
                ("question_id", "=", question.id),
            ]
        )

        if question.question_type in ("binary", "multi_binary"):
            if not isinstance(answer, (list, tuple)):
                answer = [answer]
            for answer_binary in answer:
                old_answers = self._save_line_simple_answer(
                    question, old_answers, answer_binary
                )
        else:
            super(SurveyUserInput, self).save_lines(question, answer, comment=comment)

    def _get_line_answer_values(self, question, answer, answer_type):
        vals = super(SurveyUserInput, self)._get_line_answer_values(
            question, answer, answer_type
        )
        if answer_type in ("binary", "multi_binary") and answer:
            if answer_type == "binary":
                del vals["value_binary"]
            else:
                del vals["value_multi_binary"]
            if not isinstance(answer, (list, tuple)):
                answer = [answer]
            answer_binary_datas = []
            for answer_binary in answer:
                data = answer_binary.get("data")
                filename = answer_binary.get("filename")
                answer_binary_datas += [
                    (
                        0,
                        0,
                        {
                            "value_binary": data,
                            "filename": filename,
                        },
                    )
                ]
            vals.update({"answer_binary_ids": answer_binary_datas})
        return vals
