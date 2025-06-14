# Copyright 2024 Binhex - Adasat Torres de León
# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import timedelta

from odoo import _, api, fields, models


class SurveyLinkMixin(models.AbstractModel):
    _name = "survey.link.mixin"

    survey_answer_count = fields.Integer(
        compute="_compute_survey_answer_count",
    )
    _partner_field = "partner_id"

    @api.model
    def _check_partner_field(self, record, field):
        value = getattr(record, field, False)
        return value.id if hasattr(value, "id") else value

    def _compute_survey_answer_count(self):
        for record in self:
            record.survey_answer_count = self.env["survey.user_input"].search_count(
                [
                    ("res_id", "=", record.id),
                    ("res_model", "=", record._name),
                    (
                        "partner_id",
                        "=",
                        self._check_partner_field(record, record._partner_field),
                    ),
                ]
            )

    def action_view_survey_answer(self):
        self.ensure_one()
        action = self.env.ref("survey.action_survey_user_input").read()[0]
        action["domain"] = [
            ("res_id", "=", self.id),
            ("res_model", "=", self._name),
            ("partner_id", "=", self._check_partner_field(self, self._partner_field)),
        ]
        action["context"] = {
            "default_res_id": self.id,
            "default_res_model": self._name,
            "default_partner_id": self._check_partner_field(
                self,
                self._partner_field,
            ),
            "default_survey_id": self.get_default_survey(),
        }
        return action

    # Override this method if you need to add a default survey.
    def get_default_survey(self):
        return False

    # This method return False if you haven't a default_survey
    def get_share_link(self):
        self.ensure_one()
        survey_link_wizard = self.env["survey.link.wizard"].create(
            {
                "res_id": self.id,
                "res_model": self._name,
                "partner_id": self._check_partner_field(self, self._partner_field),
                "date_deadline": fields.Date.today() + timedelta(days=5),
                "survey_id": self.get_default_survey(),
            }
        )
        return survey_link_wizard.share_link if survey_link_wizard else False

    def action_survey_link_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Survey Share Link"),
            "res_model": "survey.link.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_res_id": self.id,
                "default_res_model": self._name,
                "default_partner_id": self._check_partner_field(
                    self, self._partner_field
                ),
                "default_date_deadline": fields.Date.today(),
                "default_survey_id": self.get_default_survey(),
            },
        }
