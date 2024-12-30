# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    def _create_answer(
        self,
        user=False,
        partner=False,
        email=False,
        test_entry=False,
        res_id=False,
        res_model=False,
        check_attempts=True,
        **additional_vals
    ):
        user_inputs = super()._create_answer(
            user=user,
            partner=partner,
            email=email,
            test_entry=test_entry,
            **additional_vals
        )
        vals = {}
        if res_id:
            vals["res_id"] = res_id
        if res_model:
            vals["res_model"] = res_model
        if vals:
            user_inputs.write(vals)
        return user_inputs
