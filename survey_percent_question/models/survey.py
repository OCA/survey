# -*- coding: utf-8 -*-
# Copyright 2015 Savoir-faire Linux
# Copyright 2016 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict

from openerp import api, models
from openerp.tools.translate import _


class Survey(models.Model):
    _inherit = 'survey.survey'

    @api.model
    def prepare_result(self, question, current_filters=None):
        """
        Compute statistical data for questions by counting number of vote per
        choice on basis of filter
        """
        current_filters = current_filters if current_filters else []
        result_summary = {}

        if question.type == 'percent_split':
            header = []
            order = {}
            idx = 0
            for idx, label in enumerate(question.labels_ids):
                order[label.id] = idx
                header.append(label.value)

            if question.comments_allowed:
                header.extend([_("Other"), _("Comment")])
                order["comment_value"] = idx + 1
                order["comment_label"] = idx + 2

            result_summary["header"] = header

            data = defaultdict(lambda: [''] * len(header))
            all_lines = [
                line
                for line in question.user_input_line_ids
                if not(current_filters) or
                line.user_input_id.id in current_filters
            ]

            for line in all_lines:
                row = data[line.user_input_id]
                if line.value_suggested_row:
                    idx = order[line.value_suggested_row.id]
                    row[idx] = line.value_number
                elif "comment_value" in order:
                    row[order["comment_value"]] = line["value_number"]
                    row[order["comment_label"]] = line["value_text"]
            result_summary["data"] = list(data.values())
        else:
            return super(Survey, self).prepare_result(
                question, current_filters=current_filters)

        return result_summary
