# Copyright <2020> PESOL <info@pesol.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

import logging
from datetime import datetime

from odoo import api, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class Survey(models.Model):
    _description = "Survey"
    _inherit = "survey.survey"

    @api.model
    def filter_input_ids(self, filters, finished=False):
        """
        Filter the Survey Inputs corresponding to the bounds defined by the
        filters
        :return: list of ids filtered by date
        """
        user_input_obj = self.env["survey.user_input"]
        date_filter = list(filter(lambda x: x.get("date_from", {}), filters))
        filters = filter(lambda x: not x.get("date_from", {}), filters)
        user_inputs = super(Survey, self).filter_input_ids(filters, finished)
        user_inputs_filtered = []
        # In case not finished filter get all the answers in the
        # bounds of the dates
        if date_filter and not user_inputs:
            user_inputs = user_input_obj.search([("survey_id", "=", self.id)])
            user_inputs = user_inputs and user_inputs.ids
        if date_filter and user_inputs:
            for user_input in user_input_obj.browse(user_inputs):
                date_from = datetime.strptime(
                    date_filter[0].get("date_from", False),
                    DEFAULT_SERVER_DATETIME_FORMAT,
                )
                date_end = datetime.strptime(
                    date_filter[0].get("date_end", False),
                    DEFAULT_SERVER_DATETIME_FORMAT,
                )
                if date_from <= user_input.create_date <= date_end:
                    user_inputs_filtered.append(user_input.id)
        return user_inputs_filtered or user_inputs

    @api.model
    def get_filter_display_data(self, filters):
        """
        Function that returns a list of dictionaries with the filters to show
        in frontend section Filters from Survey Result
        :param filters:
        :return:
        """
        date_filter = list(filter(lambda x: x.get("date_from", False), filters))
        regular_filters = filter(lambda x: not x.get("date_from", False), filters)
        filter_display_data = super(Survey, self).get_filter_display_data(
            regular_filters
        )
        # Extend the usual filters with the date range filters
        if len(list(date_filter)):
            filter_display_data.append(
                {
                    "labels": [date_filter[0].get("date_from", False)],
                    "question_text": u"Date From",
                }
            )
            if date_filter[0].get("date_end", False):
                filter_display_data.append(
                    {
                        "labels": [date_filter[0].get("date_end", False)],
                        "question_text": u"Date End",
                    }
                )
        return filter_display_data

    @api.model
    def get_input_summary(self, question, current_filters=None):
        """
        Rewrite this function to also take in consideration the date filters
        """
        result = dict()
        if current_filters:
            result["answered"] = len(
                [
                    line
                    for line in question.user_input_line_ids
                    if line.user_input_id.state != "new"
                    and not line.user_input_id.test_entry
                    and not line.skipped
                    and line.user_input_id.id in current_filters
                ]
            )
            result["skipped"] = len(
                [
                    line
                    for line in question.user_input_line_ids
                    if line.user_input_id.state != "new"
                    and not line.user_input_id.test_entry
                    and line.skipped
                    and line.user_input_id.id in current_filters
                ]
            )
        else:
            result = super(Survey, self).get_input_summary(question, current_filters)
        return result

    @api.model
    def prepare_result(self, question, current_filters=None):
        """
        Pre process the result before being displayed in frontend. Sort it to
        have in Data section the highest values on top
        """
        result = super(Survey, self).prepare_result(question, current_filters)
        if "input_lines" in result:
            result["input_lines"] = sorted(
                result["input_lines"],
                key=lambda input: input.value_number,
                reverse=True,
            )
        elif "answers" in result and isinstance(result["answers"], list):
            result["answers"] = sorted(
                result["answers"], key=lambda c: c["count"], reverse=True
            )
        return result
