# Copyright 2026 Acsone
# @author Pierre Verkest <pierre.verkest@apycod.fr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
from odoo import http
from odoo.http import request

from odoo.addons.survey_prevent_create_on_start.controllers.main import (
    SurveyPreventCreate,
)


class SurveyEdit(SurveyPreventCreate):
    def _find_existing_answer(self, survey_sudo, answer_token=None, **post):
        answer_sudo = super()._find_existing_answer(
            survey_sudo, answer_token=answer_token, **post
        )
        if (
            not answer_sudo
            and survey_sudo.allow_editing
            and not request.env.user._is_public()
        ):
            answer_sudo = (
                self.env["survey.user_input"]
                .sudo()
                .search(
                    [
                        ("survey_id", "=", survey_sudo.id),
                        ("partner_id", "=", request.env.user.partner_id.id),
                        ("test_entry", "=", False),
                    ],
                    order="create_date desc",
                    limit=1,
                )
            )
        return answer_sudo

    @http.route(
        "/survey/start/<string:survey_token>", type="http", auth="public", website=True
    )
    def survey_start(self, survey_token, answer_token=None, email=False, **post):
        survey_sudo, _survey_user_input_sudo = self._fetch_from_access_token(
            survey_token, False
        )
        if survey_sudo and survey_sudo.allow_editing:
            answer_sudo = self._find_existing_answer(
                survey_sudo, answer_token=answer_token, **post
            )
            if answer_sudo and answer_sudo.state == "done" and post.get("edit"):
                answer_sudo.action_reopen_for_edition()

            if answer_sudo and not answer_token:
                answer_token = answer_sudo.access_token

        return super().survey_start(
            survey_token, answer_token=answer_token, email=email, **post
        )

    @http.route(
        [
            "/survey/<string:survey_token>",
            "/survey/<string:survey_token>/<string:answer_token>",
        ],
        type="http",
        auth="public",
        website=True,
    )
    def survey_display_page(self, survey_token, answer_token=None, **post):
        if post.get("edit"):
            if not answer_token:
                answer_token = request.cookies.get(f"survey_{survey_token}")
            if answer_token:
                return request.redirect(
                    f"/survey/start/{survey_token}?answer_token={answer_token}&edit=1"
                )
        return super().survey_display_page(
            survey_token, answer_token=answer_token, **post
        )
