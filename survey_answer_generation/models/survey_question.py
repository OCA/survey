# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    next_survey_id = fields.Many2one(related="survey_id.next_survey_id")
    next_survey_question_id = fields.Many2one(
        comodel_name="survey.question",
        domain="[('survey_id', '=', next_survey_id), ('question_type', '=', question_type)]",
        help="Prefill this answer of the next survey with the answer of this one",
    )


class SurveyLabel(models.Model):
    _inherit = "survey.question.answer"

    next_survey_question_id = fields.Many2one(
        related="question_id.next_survey_question_id"
    )
    next_survey_question_answer_id = fields.Many2one(
        comodel_name="survey.question.answer",
        domain="[('question_id', '=', next_survey_question_id)]",
        help="Prefill this answer of the next survey with the answer of this one",
    )
