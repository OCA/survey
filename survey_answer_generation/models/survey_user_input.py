# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.tools import get_diff


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    next_survey_input_id = fields.Many2one(
        comodel_name="survey.user_input", readonly=True
    )
    origin_input_id = fields.Many2one(comodel_name="survey.user_input", readonly=True)
    diff_user_input_line_count = fields.Integer(
        compute="_compute_diff_user_input_line_count"
    )

    def save_lines(self, question, answer, comment=None):
        """Sync the answers for the next question when they're saved so we don't have
        to repeat the logic again"""
        res = super().save_lines(question, answer, comment=comment)
        if question.next_survey_question_id and self.next_survey_input_id:
            self.next_survey_input_id.with_context(
                save_next_question_answer=True
            ).save_lines(question.next_survey_question_id, answer, comment)
        return res

    def _get_line_answer_values(self, question, answer, answer_type):
        """Link the answers"""
        vals = super()._get_line_answer_values(question, answer, answer_type)
        if not self.env.context.get("save_next_question_answer"):
            return vals
        # Find out the next question answer id to save it instead of the current one
        if answer_type == "suggestion":
            suggested_answer_id = vals.get("suggested_answer_id")
            if suggested_answer_id:
                suggested_answer = self.env["survey.question.answer"].browse(
                    suggested_answer_id
                )
                vals[
                    "suggested_answer_id"
                ] = suggested_answer.next_survey_question_answer_id.id
            origin_line = self.origin_input_id.user_input_line_ids.filtered(
                lambda x: x.question_id.next_survey_question_id == question
                and x.answer_type == "suggestion"
                and x.suggested_answer_id.id == suggested_answer_id
            )
        else:
            origin_line = self.origin_input_id.user_input_line_ids.filtered(
                lambda x: x.question_id.next_survey_question_id == question
            )
        if origin_line:
            vals["origin_input_line"] = origin_line.id
        return vals

    def _get_line_comment_values(self, question, comment):
        """Comments go their own way"""
        vals = super()._get_line_comment_values(question, comment)
        if self.origin_input_id and (
            origin_line := self.origin_input_id.user_input_line_ids.filtered(
                lambda x: x.question_id.next_survey_question_id == question
                and x.answer_type == "char_box"
            )
        ):
            vals["origin_input_line"] = origin_line.id
        return vals

    def _compute_diff_user_input_line_count(self):
        self.diff_user_input_line_count = False
        for user_input in self.filtered("origin_input_id"):
            user_input.diff_user_input_line_count = len(
                user_input.user_input_line_ids.filtered("diff_with_origin")
            )

    def _mark_done(self):
        """Ensure that the contact info matches for both surveys"""
        res = super()._mark_done()
        if (
            self.next_survey_input_id
            and self.next_survey_input_id.partner_id != self.partner_id
        ):
            self.next_survey_input_id.partner_id = self.partner_id
            self.next_survey_input_id.email = self.email
        return res


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    origin_input_line = fields.Many2one(comodel_name="survey.user_input.line")
    diff_with_origin = fields.Html(
        compute="_compute_diff_with_origin",
        store=True,
    )

    @api.depends(
        *[
            f"value_{x}"
            for x in {"char_box", "text_box", "numerical_box", "date", "datetime"}
        ]
    )
    def _compute_diff_with_origin(self):
        """When two answers are linked the next survey question is prefilled. If the
        user changes the answer in the next survey we want to spot the difference"""
        self.diff_with_origin = False
        for line in self.filtered("origin_input_line"):
            if line.answer_type and line.answer_type != "suggestion":
                value = f"value_{line.answer_type}"
                previous_value = str(line.origin_input_line[value])
                current_value = str(line[value])
            else:
                current_value = line.suggested_answer_id.value
                previous_value = line.origin_input_line.suggested_answer_id.value
            if previous_value == current_value:
                continue
            line.diff_with_origin = get_diff(
                (previous_value, _("Previous")), (current_value, _("Current"))
            )
