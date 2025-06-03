# Copyright 2025 Kencove - Mohamed Alkobrosli
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    suggested_prefilled_answer = fields.Char()
    suggested_prefilled_answer_multi = fields.Text()
