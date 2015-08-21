# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    survey_input_lines = fields.One2many(
        comodel_name='survey.user_input_line', inverse_name='partner_id',
        string='Surveys answers')
    survey_inputs = fields.One2many(
        comodel_name='survey.user_input', inverse_name='partner_id',
        string='Surveys')
    survey_input_count = fields.Integer(
        string='Survey number', compute='_count_survey_input',
        store=True)

    @api.one
    @api.depends('survey_inputs')
    def _count_survey_input(self):
        self.survey_input_count = len(self.survey_inputs)
