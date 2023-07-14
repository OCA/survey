# Copyright 2023 Jose Zambudio - Aures Tic <jose@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    answer_type = fields.Selection(
        selection_add=[
            ("binary", "Binary"),
            ("multi_binary", "Multi: Binary"),
        ]
    )
    answer_binary_ids = fields.One2many(
        comodel_name="survey.user_input.line_binary",
        inverse_name="input_line_id",
        readonly=True,
    )

    @api.constrains("skipped", "answer_type")
    def _check_answer_type_skipped(self):
        super_check = self
        for line in self:
            if line.answer_type not in ("binary", "multi_binary"):
                continue
            super_check -= line
            field_name = "answer_binary_ids"
            if field_name and not line[field_name]:
                raise ValidationError(_("The answer must be in the right type"))
        return super(SurveyUserInputLine, super_check)._check_answer_type_skipped()

    @api.constrains(
        "question_id",
        "answer_type",
        "answer_binary_ids",
    )
    def _check_binary_answer(self):
        for rec in self:
            if (
                rec.question_id.question_type not in ("binary", "multi_binary")
                or not rec.answer_type
                or rec.answer_type not in ("binary", "multi_binary")
            ):
                continue
            for answer_binary in rec.answer_binary_ids:
                if (
                    rec.question_id.max_filesize
                    and rec.question_id.max_filesize < answer_binary.value_binary_size
                ):
                    raise ValidationError(
                        _("The file cannot exceed {}MB in size.").format(
                            rec.question_id.max_filesize / 1024 / 1024
                        )
                    )
                if (
                    rec.question_id.allowed_filemimetypes
                    and answer_binary.value_binary_type
                    not in rec.question_id.allowed_filemimetypes
                ):
                    raise ValidationError(
                        _("Only files with {} mime types are allowed.").format(
                            rec.question_id.allowed_filemimetypes
                        )
                    )
