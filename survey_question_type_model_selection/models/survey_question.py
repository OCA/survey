# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import ast

from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_type = fields.Selection(selection_add=[("model", "Model selection")])
    question_model_id = fields.Many2one(
        string="Applies to",
        comodel_name="ir.model",
        default=lambda self: self.env["ir.model"]._get_id("res.partner"),
        domain=lambda self: [("model", "in", self._get_selectable_models())],
        ondelete="cascade",
    )
    question_model_name = fields.Char(related="question_model_id.model")
    question_domain = fields.Char(string="Filter Domain")

    @api.model
    def _get_selectable_models(self):
        return [
            name
            for name, model in self.env.registry.items()
            if not model._abstract and not model._transient
        ]

    def _get_parsed_domain(self):
        """Parse domain string safely into a Python list."""
        if not self.question_domain:
            return []
        try:
            domain = ast.literal_eval(self.question_domain)
            return domain if isinstance(domain, list) else []
        except Exception:
            return []

    def get_model_options(self):
        """Return Model options filtered by the domain."""
        self.ensure_one()
        domain = self._get_parsed_domain()
        records = self.env[self.question_model_name].sudo().search(domain)
        return [(rec.id, rec.display_name, rec._name) for rec in records]
