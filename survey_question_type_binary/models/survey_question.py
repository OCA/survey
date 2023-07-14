# Copyright 2023 Jose Zambudio - Aures Tic <jose@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64

from odoo import _, fields, models, tools
from odoo.tools.mimetypes import guess_mimetype


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_type = fields.Selection(
        selection_add=[
            ("binary", "Binary"),
            ("multi_binary", "Multiple: Binary"),
        ]
    )
    allowed_filemimetypes = fields.Char(
        help="File mime types separated by commas (E.g: image/png,image/jpeg). "
        "Leave empty to allow any value.",
    )
    max_filesize = fields.Integer(
        default="52428800",
        help="Indicate maximum file size in bytes (Default 50MB). Leave empty "
        "to allow any value.",
    )

    def validate_question(self, answer, comment=None):
        if self.question_type in ("binary", "multi_binary"):
            return self.validate_binary(answer)
        return super(SurveyQuestion, self).validate_question(answer, comment=comment)

    def validate_binary(self, answers):
        self.ensure_one()
        errors = {}
        # Empty answer to mandatory question
        if self.constr_mandatory and not answers:
            errors.update({self.id: self.constr_error_msg})
        if answers:
            if not isinstance(answers, (list, tuple)):
                answers = [answers]
            for answer in answers:
                try:
                    data = answer.get("data")
                    filesize = (
                        data and (len(data) * 3) / 4 - str(data).count("=", -2) or 0
                    )
                    filemimetype = (
                        data and guess_mimetype(base64.b64decode(data)) or False
                    )
                    answer.update(
                        {
                            "size": filesize,
                            "type": filemimetype,
                        }
                    )
                except ValueError:
                    errors.update({self.id: "This is not a file"})
                    return errors
                with tools.ignore(Exception):
                    # 0 answer to mandatory question
                    if self.constr_mandatory and not data:
                        errors.update({self.id: self.constr_error_msg})
                    else:
                        if (
                            self.allowed_filemimetypes
                            and filemimetype not in self.allowed_filemimetypes
                        ):
                            errors.update(
                                {
                                    self.id: _(
                                        "Only files with {} mime types are allowed."
                                    ).format(self.allowed_filemimetypes)
                                }
                            )
                        if self.max_filesize and filesize > self.max_filesize:
                            errors.update(
                                {
                                    self.id: _(
                                        "The file cannot exceed {}MB in size."
                                    ).format(self.max_filesize / 1024 / 1024)
                                }
                            )
        return errors
