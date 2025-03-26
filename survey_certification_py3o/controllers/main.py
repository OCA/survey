# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import SUPERUSER_ID
from odoo.http import content_disposition, request

from odoo.addons.survey.controllers.main import Survey


class Survey(Survey):
    def _generate_report(self, user_input, download=True):
        if not user_input.py3o_template_id:
            return super()._generate_report(user_input, download=download)
        report = (
            request.env.ref("survey_certification_py3o.custom_certification_report")
            .with_user(SUPERUSER_ID)
            ._render_py3o([user_input.id], data={"report_type": "pdf"})[0]
        )
        report_content_disposition = content_disposition("Certification.pdf")
        if not download:
            content_split = report_content_disposition.split(";")
            content_split[0] = "inline"
            report_content_disposition = ";".join(content_split)
        return request.make_response(
            report,
            headers=[
                ("Content-Type", "application/pdf"),
                ("Content-Length", len(report)),
                ("Content-Disposition", report_content_disposition),
            ],
        )
