# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SurveyQuestion(models.Model):

    _inherit = "survey.question"

    def _validate_text_box(self, answer):
        # Text box answer validation
        # Length of the answer must be in a range
        if self.validation_required:
            if not (
                self.validation_length_min <= len(answer) <= self.validation_length_max
            ):
                return {self.id: self.validation_error_msg}
        return {}

    def validate_question(self, answer, comment=None):
        """
        Validate text box questions too.
        """
        res = super().validate_question(answer, comment)
        if not res and self.question_type == "text_box":
            return self._validate_text_box(answer)
        return res
