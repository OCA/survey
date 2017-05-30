# -*- coding: utf-8 -*-
# Copyright (c) 2015 Antonio Espinosa <antonioea@antiun.com>
# Copyright 2016 Camptocamp SA - Damien Crier
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    partner_id = fields.Many2one(related='user_input_id.partner_id',
                                 store=True)
