# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyRepresentativeMixin(models.AbstractModel):
    """This abstract is handy when we have a generated record that is linked to a
    user input. This way, we can compute the represetative partner right away"""

    _name = "survey.representative.mixin"
    _description = "Use this mixin in models that have a linked survey input"

    survey_user_input_id = fields.Many2one(
        comodel_name="survey.user_input", readonly=True
    )
    survey_representative_partner_id = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_survey_representative_partner_id",
        store=True,
        readonly=False,
    )

    @api.depends("survey_user_input_id")
    def _compute_survey_representative_partner_id(self):
        """Users can set the field independently of the answer, but the answer rules"""
        for record in self:
            record.survey_representative_partner_id = (
                record.survey_user_input_id.representative_partner_id
            )
