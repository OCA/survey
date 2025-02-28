import ast
import logging

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    model_id = fields.Many2one("ir.model", string="Model")
    model_name = fields.Char(related="model_id.model")
    fill_domain = fields.Char("Domain", default="[]")
    answer_values_type = fields.Selection(
        [("no", "No values"), ("value", "Value"), ("record", "Record")],
        string="Associate value to answer",
        default="no",
        required=True,
    )

    @api.onchange("model_id")
    def onchange_model_id(self):
        self.fill_domain = "[]"
        if self.model_id:
            rec = self.env[self.model_id.model].search([], limit=1)
            if not rec:
                raise UserError(_("No record found in %s", self.model_id.name))
            else:
                for answer in self.suggested_answer_ids:
                    answer.record_id = f"{self.model_id.model},{rec.id}"

    def fill(self):
        for question in self:
            if question.model_id:
                new_suggested_answer_ids = [Command.clear()]
                record_model = question.model_id.model

                if question.fill_domain:
                    domain = ast.literal_eval(question.fill_domain)
                else:
                    domain = []

                records = self.env[record_model].search(domain)

                new_suggested_answer_ids += [
                    Command.create(
                        {
                            "value": record.display_name,
                            "record_id": f"{record_model},{record.id}",
                        }
                    )
                    for record in records
                ]
                question.suggested_answer_ids = new_suggested_answer_ids
