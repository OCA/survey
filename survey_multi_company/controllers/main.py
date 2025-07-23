# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.addons.survey.controllers.main import Survey


class SurveyMultiCompany(Survey):
    def _get_access_data(self, survey_token, answer_token, ensure_token=True):
        # Web survey access in multi-company environments may lack an explicit active
        # company, causing request.env.company to default to the user's default company
        # or the first allowed one. This can lead to incorrect rule evaluation, access
        # errors, or company-specific logic failures. To ensure consistent behavior, we
        # explicitly switch to the company assigned to the survey.
        data = super()._get_access_data(
            survey_token, answer_token, ensure_token=ensure_token
        )
        survey_sudo = data.get("survey_sudo")
        if survey_sudo and survey_sudo.company_id:
            data["survey_sudo"] = survey_sudo.with_company(survey_sudo.company_id)
            if data.get("answer_sudo"):
                data["answer_sudo"] = data["answer_sudo"].with_company(
                    survey_sudo.company_id
                )
        return data
