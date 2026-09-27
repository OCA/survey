# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.http import request, route

from odoo.addons.survey.controllers.main import Survey


class SurveyMetada(Survey):
    @route()
    def survey_submit(self, survey_token, answer_token, **post):
        """The acceptance of the legal terms has the user's footprint warranty"""
        res = super().survey_submit(survey_token, answer_token, **post)
        access_data = self._get_access_data(
            survey_token, answer_token, ensure_token=True
        )
        if access_data["validity_code"] is not True:
            return res
        answer_sudo = access_data["answer_sudo"]
        if not answer_sudo.survey_id.legal_terms:
            return res
        environ = request.httprequest.headers.environ
        answer_sudo.user_metadata = (
            f"IP: {environ.get('REMOTE_ADDR')}\n"
            f"USER_AGENT: {environ.get('HTTP_USER_AGENT')}\n"
            f"ACCEPT_LANGUAGE: {environ.get('HTTP_ACCEPT_LANGUAGE')}\n"
            f"REFERER: {environ.get('HTTP_REFERER')}\n"
        )
        return res
