# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, models
from odoo.exceptions import ValidationError


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    @api.depends("question_type", "question_model_id")
    def _compute_allowed_partner_field_domain(self):
        res = super()._compute_allowed_partner_field_domain()
        for record in self:
            if record.question_type == "model":
                record.allowed_partner_field_domain = [
                    ("model", "=", "res.partner"),
                    ("ttype", "in", ["many2one", "many2many"]),
                    ("relation", "=", record.question_model_id.model),
                    ("store", "=", True),
                    ("readonly", "=", False),
                ]
        return res

    @api.constrains("question_type", "question_model_id", "res_partner_field")
    def _check_res_partner_field_relation(self):
        for record in self:
            if (
                record.question_type == "model"
                and record.res_partner_field
                and record.res_partner_field.relation != record.question_model_id.model
            ):
                raise ValidationError(
                    _(
                        "The contact field '%(field)s' stores %(relation)s records, "
                        "but the question '%(question)s' is answered with %(model)s "
                        "records.",
                        field=record.res_partner_field.field_description,
                        relation=record.res_partner_field.relation,
                        question=record.title,
                        model=record.question_model_id.model or _("no model"),
                    )
                )
