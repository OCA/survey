# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# Part of ForgeFlow. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SurveyAddQuestionGroupWizard(models.TransientModel):
    _name = "survey.add.question.group.wizard"
    _description = "Add Question Group to Survey"

    survey_id = fields.Many2one(
        "survey.survey",
        string="Survey",
        required=True,
    )
    group_id = fields.Many2one(
        "survey.question.group",
        string="Question Group",
        required=True,
    )

    def action_confirm(self):
        """Copy the group's template questions into the survey."""
        self.ensure_one()
        survey = self.survey_id
        group = self.group_id
        max_seq = max(survey.question_and_page_ids.mapped("sequence") or [0])
        for idx, question in enumerate(group.question_ids):
            question.copy(
                {
                    "survey_id": survey.id,
                    "sequence": max_seq + idx + 1,
                    "group_id": group.id,
                }
            )
        return {"type": "ir.actions.act_window_close"}
