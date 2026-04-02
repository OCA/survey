# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# Part of ForgeFlow. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    group_id = fields.Many2one(
        "survey.question.group",
        string="Question Group",
        ondelete="set null",
        copy=False,
        help="Reusable group of template questions this question belongs to.",
    )
