# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    representative_partner_id = fields.Many2one(
        comodel_name="res.partner",
        help="This partner filled this survey on behalf of other",
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        # Remove the user information so the survey is made anonymously
        answers = super().create(vals_list)
        if (
            self.env.context.get("survey_partner_representative")
            and self.env.user.has_group(
                "survey_partner_representative.partner_representative"
            )
            and all(answers.survey_id.mapped("allow_partner_representing"))
        ):
            answers.partner_id = False
            answers.email = False
            answers.nickname = False
            answers.representative_partner_id = self.env.user.partner_id
        return answers
