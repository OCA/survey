# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    next_survey_id = fields.Many2one(
        comodel_name="survey.survey", domain="[('id', '!=', id)]"
    )

    def _create_answer(
        self,
        user=False,
        partner=False,
        email=False,
        test_entry=False,
        check_attempts=True,
        **additional_vals
    ):
        """We link the next user input right away so we can sync the responses when
        they're submitted"""
        user_inputs = super()._create_answer(
            user=user,
            partner=partner,
            email=email,
            test_entry=test_entry,
            check_attempts=check_attempts,
            **additional_vals
        )
        for user_input in user_inputs.filtered("survey_id.next_survey_id"):
            next_survey_input = user_input.survey_id.next_survey_id._create_answer(
                user=user,
                email=email,
                test_entry=test_entry,
                check_attempts=check_attempts,
                **additional_vals
            )
            user_input.next_survey_input_id = next_survey_input
            next_survey_input.origin_input_id = user_input
        return user_inputs
