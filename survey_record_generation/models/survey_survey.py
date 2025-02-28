import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    survey_record_creation_ids = fields.One2many(
        "survey.record.creation",
        "survey_id",
        "Records creation",
        help="List of records created when survey submitted",
    )
