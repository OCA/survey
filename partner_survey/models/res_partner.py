# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    survey_input_lines = fields.One2many(
        comodel_name='survey.user_input_line', inverse_name='partner_id',
        string='Surveys answers')
    survey_inputs = fields.One2many(
        comodel_name='survey.user_input', inverse_name='partner_id',
        string='Surveys')
    survey_input_count = fields.Integer(
        string='Survey number', compute='_compute_survey_input_count',
        store=True)

    @api.depends('survey_inputs')
    def _compute_survey_input_count(self):
        for survey in self:
            survey.survey_input_count = len(survey.survey_inputs)
