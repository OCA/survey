# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import Counter
from odoo import api, models


class SurveySurvey(models.Model):

    _inherit = "survey.survey"

    @api.model
    def prepare_result(self, question, current_filters=None):
        """
            Compute statistical data for questions by counting number of
            vote per choice on basis of filter
        """
        current_filters = current_filters if current_filters else []
        result_summary = {}
        if question.type == "star_rate":
            result_summary = {"input_lines": []}
            all_inputs = []
            for input_line in question.user_input_line_ids:
                if (
                    not (current_filters)
                    or input_line.user_input_id.id in current_filters
                ):
                    all_inputs.append(input_line.value_number)
                    result_summary["input_lines"].append(input_line)
            if all_inputs:
                result_summary.update(
                    {
                        "average": round(sum(all_inputs) / len(all_inputs), 2),
                        "max": round(max(all_inputs), 2),
                        "min": round(min(all_inputs), 2),
                        "sum": sum(all_inputs),
                        "most_common": Counter(all_inputs).most_common(5),
                    }
                )
            return result_summary
        return super(SurveySurvey, self).prepare_result(
            question, current_filters
        )
