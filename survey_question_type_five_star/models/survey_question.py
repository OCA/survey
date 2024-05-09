# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import collections

from odoo import fields, models, tools


class SurveyQuestion(models.Model):

    _inherit = "survey.question"

    question_type = fields.Selection(
        selection_add=[("star_rate", "Five Stars Rating")], ondelete={"foo": "set null"}
    )

    def _get_stats_summary_data(self, user_input_lines):
        stats = super()._get_stats_summary_data(user_input_lines)
        if self.question_type in ["star_rate"]:
            stats.update(self._get_stats_summary_data_numerical(user_input_lines))
            stats.update(
                {
                    "common_lines": collections.Counter(
                        user_input_lines.filtered(lambda line: not line.skipped).mapped(
                            "value_numerical_box"
                        )
                    ).most_common(5),
                    "right_inputs_count": len(
                        user_input_lines.filtered(
                            lambda line: line.answer_is_correct
                        ).mapped("user_input_id")
                    ),
                }
            )
        return stats

    def validate_star_rate(self, post, answer_tag):
        self.ensure_one()
        errors = {}
        answer = post[answer_tag].strip()
        # Empty answer to mandatory question
        if self.constr_mandatory and not answer:
            errors.update({answer_tag: self.constr_error_msg})
        # Checks if user input is a number
        if answer:
            try:
                floatanswer = float(answer)
            except ValueError:
                errors.update({answer_tag: "This is not a number"})
                return errors
            # Answer is not in the right range
            with tools.ignore(Exception):
                # 0 answer to mandatory question
                if self.constr_mandatory:
                    if floatanswer == 0:
                        errors.update({answer_tag: self.constr_error_msg})
                if not (0 <= floatanswer <= 5):
                    errors.update({answer_tag: "Answer is not in the right range"})
        return errors
