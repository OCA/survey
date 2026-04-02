# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# Part of ForgeFlow. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SurveyQuestionGroup(models.Model):
    _name = "survey.question.group"
    _description = "Survey Question Group"

    name = fields.Char(required=True, translate=True)
    question_ids = fields.One2many(
        "survey.question",
        "group_id",
        string="Questions",
        domain=[("survey_id", "=", False)],
    )
