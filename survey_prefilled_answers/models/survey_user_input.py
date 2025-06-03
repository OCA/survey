# Copyright 2025 Kencove - Mohamed Alkobrosli
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import textwrap

from odoo import _, api, fields, models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    def render_answer(self, suggested_answer_id):
        partner = self.user_input_id.partner_id
        suggested_answer_value = suggested_answer_id.value
        render_env = self.env["mail.render.mixin"].sudo()
        rendered_answer = render_env._render_template(
            suggested_answer_value, partner._name, [partner.id]
        )[partner.id]
        return rendered_answer or False

    @api.depends("answer_type")
    def _compute_display_name(self):
        for line in self:
            if line.answer_type == "char_box":
                line.display_name = line.value_char_box
            elif line.answer_type == "text_box" and line.value_text_box:
                line.display_name = textwrap.shorten(
                    line.value_text_box, width=50, placeholder=" [...]"
                )
            elif line.answer_type == "numerical_box":
                line.display_name = line.value_numerical_box
            elif line.answer_type == "date":
                line.display_name = fields.Date.to_string(line.value_date)
            elif line.answer_type == "datetime":
                line.display_name = fields.Datetime.to_string(line.value_datetime)
            elif line.answer_type == "suggestion":
                rendered_answer = self.render_answer(line.suggested_answer_id)
                if line.matrix_row_id:
                    line.display_name = "%s: %s" % (
                        line.suggested_answer_id.value,
                        line.matrix_row_id.value,
                    )
                else:
                    line.display_name = (
                        rendered_answer or line.suggested_answer_id.value
                    )
            if not line.display_name:
                line.display_name = _("Skipped")
