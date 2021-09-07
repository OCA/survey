# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class SurveyQuestion(models.Model):

    _inherit = "survey.question"

    question_type = fields.Selection(selection_add=[("nps_rate", "NPS Rating")])

    def validate_nps_rate(self, post, answer_tag):
        self.ensure_one()
        errors = {}
        answer = post[answer_tag].strip()
        # Empty answer to mandatory question
        if self.constr_mandatory and not answer:
            errors.update({answer_tag: self.constr_error_msg})
        # Checks if user input is a number
        if answer:
            try:
                floatanswer = float(answer)
            except ValueError:
                errors.update({answer_tag: "This is not a number"})
            # Answer is not in the right range
            with tools.ignore(Exception):
                floatanswer = float(answer)
                # 0 answer to mandatory question
                if self.constr_mandatory:
                    if floatanswer == 0:
                        errors.update({answer_tag: self.constr_error_msg})
                if not (0 <= floatanswer <= 10):
                    errors.update({answer_tag: "Answer is not in the right range"})
        return errors
