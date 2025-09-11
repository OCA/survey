# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _prepare_partner(self):
        """Extract partner values from the answers"""
        self.ensure_one()
        elegible_inputs = self.user_input_line_ids.filtered(
            lambda x: x.question_id.res_partner_field and not x.skipped
        )
        basic_inputs = elegible_inputs.filtered(
            lambda x: x.answer_type not in {"suggestion"}
            and x.question_id.res_partner_field.name not in {"comment", "company_name"}
        )
        vals = {
            line.question_id.res_partner_field.name: line[f"value_{line.answer_type}"]
            for line in basic_inputs
        }
        for line in elegible_inputs - basic_inputs:
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
            # Create the parent company
            elif field_name == "company_name" and self.survey_id.create_parent_contact:
                if line[f"value_{line.answer_type}"]:
                    vals["parent_id"] = (
                        self.env["res.partner"]
                        .create(
                            {
                                "name": line[f"value_{line.answer_type}"],
                                "company_type": "company",
                            }
                        )
                        .id
                    )
            else:
                if line.question_id.question_type == "multiple_choice":
                    if not vals.get(field_name):
                        vals[field_name] = line.suggested_answer_id.value
                    else:
                        vals[field_name] += line.suggested_answer_id.value
                else:
                    vals[field_name] = line.suggested_answer_id.value
        vals["generating_survey_user_input_id"] = self.id
        return vals

    def _create_contact_post_process(self, partner):
        """After creating the lead send an internal message with the input link"""
        partner.message_post_with_source(
            "mail.message_origin_link",
            render_values={"self": partner, "origin": self.survey_id},
            subtype_xmlid="mail.mt_note",
        )

    def _get_existing_partner(self, email, limit=1):
        """Hook method that can be used to change the behavior of contact generation"""
        return self.env["res.partner"].search([("email", "=ilike", email)], limit=limit)

    def _mark_done(self):
        """Generate the contact when the survey is submitted"""
        for user_input in self.filtered(
            lambda r: r.survey_id.generate_contact and not r.partner_id
        ):
            vals = user_input._prepare_partner()
            partner = False
            email = vals.get("email")
            if email:
                partner = self._get_existing_partner(email)
            if not partner:
                partner = self.env["res.partner"].create(vals)
                self._create_contact_post_process(partner)
            self.update({"partner_id": partner.id, "email": partner.email})
        return super()._mark_done()
