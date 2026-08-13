# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models
from odoo.exceptions import ValidationError


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    @api.depends("question_type", "question_model_id")
    def _compute_allowed_crm_lead_field_domain(self):
        res = super()._compute_allowed_crm_lead_field_domain()
        for record in self:
            if record.question_type == "model":
                record.allowed_crm_lead_field_domain = [
                    ("model", "=", "crm.lead"),
                    ("ttype", "in", ["many2one", "many2many"]),
                    ("relation", "=", record.question_model_id.model),
                    ("store", "=", True),
                    ("readonly", "=", False),
                ]
        return res

    @api.constrains("question_type", "question_model_id", "crm_lead_field")
    def _check_crm_lead_field_relation(self):
        for record in self:
            if (
                record.question_type == "model"
                and record.crm_lead_field
                and record.crm_lead_field.relation != record.question_model_id.model
            ):
                raise ValidationError(
                    self.env._(
                        "The contact field '%(field)s' stores %(relation)s records, "
                        "but the question '%(question)s' is answered with %(model)s "
                        "records.",
                        field=record.crm_lead_field.field_description,
                        relation=record.crm_lead_field.relation,
                        question=record.title,
                        model=record.question_model_id.model or self.env._("no model"),
                    )
                )
