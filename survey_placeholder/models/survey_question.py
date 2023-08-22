# Copyright Odoo S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_placeholder = fields.Char(
        string="Placeholder",
        translate=True,
        compute="_compute_question_placeholder",
        store=True,
        readonly=False,
    )

    @api.depends("question_type")
    def _compute_question_placeholder(self):
        for question in self:
            if (
                question.question_type in ("simple_choice", "multiple_choice", "matrix")
                or not question.question_placeholder
            ):  # avoid CacheMiss errors
                question.question_placeholder = False
