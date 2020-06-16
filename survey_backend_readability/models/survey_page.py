# Copyright 2020 Le Filament (<https://www.le-filament.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SurveyPageReadability(models.Model):
    _inherit = "survey.page"

    # ------------------------------------------------------
    # Buttons
    # ------------------------------------------------------
    @api.multi
    def action_page_questions(self):
        tree_view = self.env.ref('survey_backend_readability.\
                                 survey_question_backend_readability_tree').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Questions: ' + self.title,
            'res_model': 'survey.question',
            'view_type': 'form',
            "views": [[tree_view, "tree"], [False, "form"]],
            'domain': [('page_id', '=', self.id)],
            'context': {
                'default_survey_id': self.survey_id.id,
                'default_page_id': self.id,
            },
        }
