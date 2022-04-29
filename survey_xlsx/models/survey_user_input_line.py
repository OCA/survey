# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input_line"

    def _get_xlsx_value(self):
        if self.answer_type == "suggestion":
            return self.value_suggested.display_name
        if self.answer_type == "date":
            return self.value_date.isoformat()
        return self["value_%s" % self.answer_type]
