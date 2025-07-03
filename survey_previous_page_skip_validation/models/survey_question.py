# Copyright 2025 Binhex - Adasat Torres de Leon
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    def validate_question(self, answer, comment=None):
        if not answer:
            if self.constr_mandatory and self.survey_id.users_can_go_back:
                return {}
        return super().validate_question(answer, comment)
