# Copyright 2023 Jose Zambudio - Aures Tic <jose@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64

from odoo import api, fields, models
from odoo.tools.mimetypes import guess_mimetype

VALID_MIMETYPES = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/bmp",
    "image/svg+xml",
    "image/x-icon",
]


class SurveyUserInputLineBinary(models.Model):
    _name = "survey.user_input.line_binary"
    _description = "Survey User Input Line Binary"

    input_line_id = fields.Many2one(
        comodel_name="survey.user_input.line",
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    value_binary = fields.Binary(
        required=True,
        readonly=True,
    )
    filename = fields.Char(
        required=True,
        readonly=True,
    )
    value_binary_type = fields.Char(
        compute="_compute_binary_data",
        store=True,
        readonly=True,
    )
    value_binary_size = fields.Integer(
        compute="_compute_binary_data",
        store=True,
        readonly=True,
    )
    is_binary_image = fields.Boolean(
        compute="_compute_binary_data",
        store=True,
        readonly=True,
    )

    @api.depends("value_binary")
    def _compute_binary_data(self):
        for input_line in self:
            input_line.value_binary_type = guess_mimetype(
                base64.b64decode(input_line.value_binary)
            )
            input_line.value_binary_size = (len(input_line.value_binary) * 3) / 4 - str(
                input_line.value_binary
            ).count("=", -2)
            input_line.is_binary_image = input_line.value_binary_type in VALID_MIMETYPES

    def download_binary(self):
        url = "/web/content/?model=survey.user_input.line_binary&download=true"
        field_data = "&filename_field=filename&field=value_binary"
        file_data = f"&id={self.id}&filename={self.filename}"
        return {
            "type": "ir.actions.act_url",
            "url": url + field_data + file_data,
            "target": "new",
            "close": True,
        }
