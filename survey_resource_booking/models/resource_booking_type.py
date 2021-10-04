# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResourceBookingType(models.Model):
    _inherit = "resource.booking.type"

    survey_id = fields.Many2one(
        "survey.survey",
        string="Survey",
        track_visibility="onchange",
        help="You will be able to invite requesters to respond to this survey.",
    )
