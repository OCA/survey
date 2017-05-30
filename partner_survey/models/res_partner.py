# -*- coding: utf-8 -*-
# Copyright (c) 2015 Antonio Espinosa <antonioea@antiun.com>
# Copyright 2016 Camptocamp SA - Damien Crier
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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
        string='Survey number', compute='_count_survey_input',
        store=True)

    @api.one
    @api.depends('survey_inputs')
    def _count_survey_input(self):
        self.survey_input_count = len(self.survey_inputs)
