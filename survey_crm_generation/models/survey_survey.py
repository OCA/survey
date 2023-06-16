# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    generate_leads = fields.Boolean(
        help="Generate leads/opportunities linked to the generated quotations",
    )
    crm_tag_ids = fields.Many2many(
        comodel_name="crm.tag",
        help="Set the default crm tags in the generated leads/opportunities",
    )
    crm_team_id = fields.Many2one(comodel_name="crm.team")
