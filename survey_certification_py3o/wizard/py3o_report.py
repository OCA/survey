# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from base64 import b64decode

from odoo import models


class Py3oReport(models.TransientModel):
    _inherit = "py3o.report"

    def _get_template_fallback(self, model_instance):
        if (
            model_instance._name == "survey.user_input"
            and model_instance.py3o_template_id
        ):
            return b64decode(model_instance.py3o_template_id.py3o_template_data)
        return super()._get_template_fallback(model_instance)
