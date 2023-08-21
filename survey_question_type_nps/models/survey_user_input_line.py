# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def save_lines(self, question, answer, comment=None):
        old_answers = self.env["survey.user_input.line"].search(
            [("user_input_id", "=", self.id), ("question_id", "=", question.id)]
        )

        if question.question_type in ["nps_rate"]:
            return self._save_line_simple_answer(question, old_answers, answer)
        else:
            return super(SurveyUserInput, self).save_lines(
                question, answer, comment=comment
            )

    def _get_line_answer_values(self, question, answer, answer_type):
        vals = super(SurveyUserInput, self)._get_line_answer_values(
            question, answer, answer_type
        )
        if answer_type == "nps_rate" and answer:
            value = float(answer)
            nps = 1 if value >= 9 else -1 if value <= 6 else 0
            vals.update(
                {
                    "value_numerical_box": float(answer),
                    "answer_type": "numerical_box",
                    "value_nps": nps,
                }
            )
            vals.pop("value_nps_rate")
        return vals


class SurveyUserInputLine(models.Model):

    _inherit = "survey.user_input.line"

    value_nps = fields.Integer()

    @api.constrains("question_id", "answer_type", "value_numerical_box")
    def _check_nps_rate_answer(self):
        for rec in self:
            if rec.question_id.question_type == "nps_rate":
                if not rec.answer_type:
                    continue
                if rec.answer_type != "numerical_box":
                    raise ValidationError(
                        _("NPS rate question must have numeric answer")
                    )
                if rec.question_id.constr_mandatory and not (
                    0 < rec.value_numerical_box <= 10
                ):
                    raise ValidationError(_("Answer is not in the right range"))
                if not rec.question_id.constr_mandatory and not (
                    0 <= rec.value_numerical_box <= 10
                ):
                    raise ValidationError(_("Answer is not in the right range"))
