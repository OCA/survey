# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    generate_contact = fields.Boolean(
        help="Generate contacts for anonymous survey users",
    )
    create_parent_contact = fields.Boolean(
        help="Set the company_name in a question and a parent contact will be "
        "created to hold the generated one",
    )
