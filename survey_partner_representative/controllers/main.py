# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.http import request

from odoo.addons.survey.controllers.main import Survey


class Survey(Survey):
    def _check_validity(
        self, survey_token, answer_token, ensure_token=True, check_partner=True
    ):
        # Avoid partner mismatching error
        survey_sudo, _answer_sudo = self._fetch_from_access_token(
            survey_token, answer_token
        )
        if survey_sudo.allow_partner_representing and request.env.user.has_group(
            "survey_partner_representative.partner_representative"
        ):
            check_partner = False
        return super()._check_validity(
            survey_token, answer_token, ensure_token, check_partner
        )
