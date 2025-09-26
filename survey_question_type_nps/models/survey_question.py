# Copyright 2018 ACSONE SA/NV
# Copyright 2025 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import collections
import contextlib

from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_type = fields.Selection(selection_add=[("nps_rate", "NPS Rating")])

    def _get_stats_summary_data(self, user_input_lines):
        stats = super()._get_stats_summary_data(user_input_lines)
        if self.question_type in ["nps_rate"]:
            stats.update(self._get_stats_summary_data_numerical(user_input_lines))
            stats.update(
                {
                    "common_lines": collections.Counter(
                        user_input_lines.filtered(lambda line: not line.skipped).mapped(
                            "value_numerical_box"
                        )
                    ).most_common(5),
                }
            )
        return stats

    def validate_question(self, answer, comment=None):
        res = super().validate_question(answer, comment)
        if answer and self.question_type == "nps_rate":
            return self._validate_nps_rate(answer)
        return res

    def _validate_nps_rate(self, answer):
        try:
            floatanswer = float(answer)
        except ValueError:
            return {self.id: self.env._("This is not a number")}
        if self.validation_required:
            # Answer is not in the right range
            with contextlib.suppress(Exception):
                if not (0 <= floatanswer <= 10):
                    return {
                        self.id: self.validation_error_msg
                        or self.env._("Answer is not in the right range")
                    }
        return {}
