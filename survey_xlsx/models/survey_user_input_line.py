# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    def _get_xlsx_value(self):
        if self.answer_type == "suggestion":
            return self.suggested_answer_id.display_name
        if self.answer_type == "date":
            return self.value_date.isoformat()
        return self["value_%s" % self.answer_type]
