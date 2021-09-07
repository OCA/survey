# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SurveyUserInputLine(models.Model):

    _inherit = "survey.user_input_line"

    value_nps = fields.Integer()

    @api.model
    def save_line_nps_rate(self, user_input_id, question, post, answer_tag):
        vals = {
            "user_input_id": user_input_id,
            "question_id": question.id,
            "survey_id": question.survey_id.id,
            "skipped": False,
        }
        if answer_tag in post and post[answer_tag].strip():
            value = float(post[answer_tag])
            nps = 1 if value >= 9 else -1 if value <= 6 else 0
            vals.update(
                {"answer_type": "number", "value_number": value, "value_nps": nps}
            )
        else:
            vals.update({"answer_type": None, "skipped": True})
        old_uil = self.search(
            [
                ("user_input_id", "=", user_input_id),
                ("survey_id", "=", question.survey_id.id),
                ("question_id", "=", question.id),
            ]
        )
        if old_uil:
            old_uil.write(vals)
        else:
            old_uil.create(vals)
        return True

    @api.constrains("question_id", "answer_type", "value_number")
    def _check_nps_rate_answer(self):
        for rec in self:
            if rec.question_id.question_type == "nps_rate":
                if rec.answer_type != "number":
                    raise ValidationError(
                        _("NPS rate question must have numeric answer")
                    )
                if rec.question_id.constr_mandatory and not (
                    0 < rec.value_number <= 10
                ):
                    raise ValidationError(_("Answer is not in the right range"))
                if not rec.question_id.constr_mandatory and not (
                    0 <= rec.value_number <= 10
                ):
                    raise ValidationError(_("Answer is not in the right range"))
