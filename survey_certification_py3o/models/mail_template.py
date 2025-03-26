# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    def generate_email(self, res_ids, fields=None):
        self.ensure_one()
        if (
            self.model == "survey.user_input"
            and self.env["survey.user_input"].browse(res_ids).py3o_template_id
        ):
            self.report_template = self.env.ref(
                "survey_certification_py3o.custom_certification_report"
            )
        return super().generate_email(res_ids, fields=fields)
