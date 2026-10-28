# Copyright 2026 Acsone
# @author Pierre Verkest <pierre.verkest@apycod.fr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import http
from odoo.http import request

from odoo.addons.survey.controllers.main import Survey


class SurveyPreventCreate(Survey):
    def _find_existing_answer(self, survey_sudo, answer_token=None, **post):
        """Hook to find a pre-existing answer for the current request.

        By default, relies on answer_token and session cookies via _get_access_data.
        Can be overridden by downstream modules (e.g. survey_user_input_edit)
        to resolve an answer from custom context (user, session, etc.).
        """
        if not answer_token:
            answer_token = request.cookies.get(f"survey_{survey_sudo.access_token}")

        access_data = self._get_access_data(
            survey_sudo.access_token, answer_token, ensure_token=False
        )
        return access_data.get("answer_sudo")

    @http.route(
        "/survey/start/<string:survey_token>", type="http", auth="public", website=True
    )
    def survey_start(self, survey_token, answer_token=None, email=False, **post):
        survey_sudo, _user_input_sudo = self._fetch_from_access_token(
            survey_token, False
        )
        if survey_sudo and survey_sudo.prevent_create_on_start:
            answer_sudo = self._find_existing_answer(
                survey_sudo, answer_token=answer_token, **post
            )
            if not answer_sudo:
                return request.render(
                    "survey_prevent_create_on_start.survey_cannot_create_answer",
                    {"survey": survey_sudo},
                )
            if not answer_token:
                answer_token = answer_sudo.access_token

        return super().survey_start(
            survey_token, answer_token=answer_token, email=email, **post
        )
