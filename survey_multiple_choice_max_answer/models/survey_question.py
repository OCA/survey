# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SurveyQuestion(models.Model):

    _inherit = "survey.question"

    validation_multiple_answers_min = fields.Integer("Minimum Number of Answers")
    validation_multiple_answers_max = fields.Integer("Maximum Number of Answers")

    _sql_constraints = [
        (
            "non_neg_multiple_ans_min",
            "CHECK (validation_multiple_answers_min >= 0)",
            "The minimum number of answers must be non-negative!",
        ),
        (
            "non_neg_multiple_ans_max",
            "CHECK (validation_multiple_answers_max >= 0)",
            "The maximum number of answers must be non-negative!",
        ),
        (
            "validation_multiple_ans",
            "CHECK (validation_multiple_answers_min <= validation_multiple_answers_max)",
            "Max number of multiple answers cannot be smaller "
            "than min number of multiple answers!",
        ),
    ]

    def _validate_choice(self, answer, comment):
        res = super()._validate_choice(answer, comment)
        if res or self.question_type != "multiple_choice":
            return res

        # When only 1 suggested answer is received from website in controller,
        # it should be given as a list of length 1: [sugg_ans_id],
        # but it is given as a string: str(sugg_ans_id)
        answer_count = len(answer) if isinstance(answer, list) else 1
        if (
            self.validation_required
            and self.validation_multiple_answers_max > 0
            and not (
                self.validation_multiple_answers_min
                <= answer_count
                <= self.validation_multiple_answers_max
            )
        ):
            return {self.id: self.validation_error_msg}
        return res
