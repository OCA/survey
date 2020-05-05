from odoo import fields, models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input_line"

    partner_id = fields.Many2one(related="user_input_id.partner_id", store=True)
