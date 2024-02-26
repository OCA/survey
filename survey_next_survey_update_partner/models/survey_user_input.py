# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _prepare_generated_partner_update(self, lines):
        basic_inputs = lines.filtered(
            lambda x: x.answer_type not in {"suggestion"}
            and x.question_id.res_partner_field.name not in {"comment"}
        )
        vals = {
            line.question_id.res_partner_field.name: line[f"value_{line.answer_type}"]
            for line in basic_inputs
        }
        for line in lines - basic_inputs:
            field_name = line.question_id.res_partner_field.name
            if line.question_id.res_partner_field.ttype == "many2one":
                vals[
                    field_name
                ] = line.suggested_answer_id.res_partner_field_resource_ref.id
            elif line.question_id.res_partner_field.ttype == "many2many":
                vals.setdefault(field_name, [])
                vals[field_name] += [
                    (4, line.suggested_answer_id.res_partner_field_resource_ref.id)
                ]
            # We'll use the comment field to add any other infos
            elif field_name == "comment":
                vals.setdefault("comment", "")
                value = (
                    line.suggested_answer_id.value
                    if line.answer_type == "suggestion"
                    else line[f"value_{line.answer_type}"]
                )
                vals["comment"] += f"\n{line.question_id.title}: {value}"
            else:
                if line.question_id.question_type == "multiple_choice":
                    if not vals.get(field_name):
                        vals[field_name] = line.suggested_answer_id.value
                    else:
                        vals[field_name] += line.suggested_answer_id.value
                else:
                    vals[field_name] = line.suggested_answer_id.value
        return vals

    def _mark_done(self):
        """Update the contact in the previous survey if any"""
        for user_input in self.filtered(
            lambda x: x.origin_input_id
            and x.partner_id.generating_survey_user_input_id == x.origin_input_id
        ):
            lines = user_input.user_input_line_ids.filtered(
                lambda x: not x.skipped
                and (
                    # Answered in the previous survey and with partner field
                    (
                        x.diff_with_origin
                        and x.origin_input_line.question_id.res_partner_field
                        and x.question_id.res_partner_field
                    )
                    # Not in previous but with partner field
                    or (not x.origin_input_line and x.question_id.res_partner_field)
                )
            )
            vals = self._prepare_generated_partner_update(lines)
            comment = vals.pop("comment", None)
            company_name = vals.pop("company_name", None)
            user_input.partner_id.update(self._prepare_generated_partner_update(lines))
            if comment:
                user_input.partner_id.comment += _(
                    "\nUpdated comment\n %(comment)s", comment=comment
                )
            if (
                company_name
                and user_input.origin_input_id.survey_id.create_parent_contact
            ):
                user_input.partner_id.parent_id.name = company_name
            elif company_name:
                user_input.partner_id.company_name = company_name
        return super()._mark_done()
