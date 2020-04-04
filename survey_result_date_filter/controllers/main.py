# Copyright <2020> PESOL <info@pesol.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

import logging
from datetime import datetime

from odoo import _, fields, tools
from odoo.exceptions import UserError

from odoo.addons.survey.controllers.main import Survey

_logger = logging.getLogger(__name__)


class CustomeSurvey(Survey):
    def validate_and_combine_date(self, date_str, time_str):
        """
        Combine date and time and return a string with well formed date
        """
        try:
            date = datetime.strptime(
                "{} {}".format(date_str, time_str), tools.DEFAULT_SERVER_DATETIME_FORMAT
            )
        except ValueError:
            raise UserError(_("Error processing date {}".format(date_str)))
        return datetime.strftime(date, tools.DEFAULT_SERVER_DATETIME_FORMAT)

    def _get_filter_data(self, post):
        """Gets the date_from and date_end parameters furthermore the rest of
        filters
        :param post:
        :return: list of filters
        """
        date_from = False
        date_end = False
        if post.get("date_from", False) or post.get("date_end", False):
            today = fields.Date.to_string(fields.Date.today())
            date_from = post.get("date_from", today)
            date_end = post.get("date_end", today)
            date_from = self.validate_and_combine_date(date_from, "00:00:00")
            post.pop("date_from", None)
            date_end = self.validate_and_combine_date(date_end, "11:59:59")
            post.pop("date_end", None)

        filters = super(CustomeSurvey, self)._get_filter_data(post)
        if date_from and date_end:
            vals = {
                "date_from": date_from,
                "date_end": date_end,
            }
            filters.append(vals)
        _logger.info("FILTERS {}".format(filters))
        return filters
