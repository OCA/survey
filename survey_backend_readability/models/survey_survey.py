# Copyright 2020 Le Filament (<https://www.le-filament.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SurveyBackendReadable(models.Model):
    _inherit = "survey.survey"

    tot_questions = fields.Integer(
        string="Number of questions",
        compute="_compute_tot_questions")

    # ------------------------------------------------------
    # Compute
    # ------------------------------------------------------
    @api.multi
    def _compute_tot_questions(self):
        for survey in self:
            survey.tot_questions = self.env['survey.question'].search_count([
                ('survey_id', '=', survey.id)])

    # ------------------------------------------------------
    # Buttons
    # ------------------------------------------------------
    @api.multi
    def action_survey_questions(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Questions',
            'res_model': 'survey.question',
            'view_type': 'form',
            "views": [[False, "tree"], [False, "form"]],
            'domain': [('survey_id', '=', self.id)],
            'context': {
                'default_survey_id': self.id,
            },
        }
