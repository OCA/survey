# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# Part of ForgeFlow. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    question_group_ids = fields.Many2many(
        "survey.question.group",
        string="Question Groups",
        help="Question groups associated with this survey.",
    )

    def action_add_question_group(self):
        """Open wizard to select a question group and add its questions."""
        self.ensure_one()
        return {
            "name": _("Add Question Group"),
            "type": "ir.actions.act_window",
            "res_model": "survey.add.question.group.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_survey_id": self.id,
            },
        }
