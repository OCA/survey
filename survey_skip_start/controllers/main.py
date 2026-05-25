# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.addons.survey.controllers.main import Survey


class Survey(Survey):
    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        survey_data = super()._prepare_survey_data(survey_sudo, answer_sudo, **post)
        survey_data["skip_start"] = survey_sudo.skip_start
        return survey_data
