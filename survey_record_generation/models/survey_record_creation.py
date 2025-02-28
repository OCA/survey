import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class SurveyRecordCreation(models.Model):
    """Configure list of models for wich record will be created on survey submission"""

    _name = "survey.record.creation"

    name = fields.Char()
    survey_id = fields.Many2one("survey.survey", string="Survey")
    model_id = fields.Many2one("ir.model", "Model", help="Model of generated record")
    field_values_ids = fields.One2many(
        "survey.record.creation.field.values",
        "survey_record_creation_id",
        string="Field values",
    )
    warning_message = fields.Html("Warning message", compute="_compute_warning_message")

    @api.onchange("model_id")
    def clear_field_values_ids(self):
        self.field_values_ids = None

    @api.depends("model_id", "field_values_ids")
    def _compute_warning_message(self):
        for record_creation in self:
            # check if all mandatory fields set
            if record_creation.model_id:
                required_field_ids = self.model_id.field_id.filtered(
                    lambda f: f.required and "property_" not in f.name
                )
                set_field_ids = self.field_values_ids.field_id
                missing_fields = required_field_ids - set_field_ids

                if missing_fields:
                    record_creation.warning_message = _(
                        "Some required fields are not set : %s",
                        ", ".join(
                            [
                                f"<b>{f.field_description}</b> (<i>{f.name}</i>)"
                                for f in missing_fields
                            ]
                        ),
                    )
                else:
                    record_creation.warning_message = None
            else:
                record_creation.warning_message = None
