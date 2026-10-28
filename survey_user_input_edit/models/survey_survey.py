# Copyright 2026 Acsone
# @author Pierre Verkest <pierre.verkest@apycod.fr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
from odoo import fields, models


class Survey(models.Model):
    _inherit = "survey.survey"

    allow_editing = fields.Boolean(
        string="Allow response editing",
        help="Allow respondents to edit their answers after submitting the survey.",
    )

    def _can_go_back(self, answer, page_or_question):
        if self.allow_editing and not self.users_can_go_back:
            if self.questions_layout == "one_page":
                return False
            if answer.state != "in_progress" or answer.is_session_answer:
                return False
            if self.page_ids and page_or_question == self.page_ids[0]:
                return False
            return (
                self.questions_layout == "page_per_section"
                or page_or_question != answer.predefined_question_ids[0]
            )
        return super()._can_go_back(answer, page_or_question)
