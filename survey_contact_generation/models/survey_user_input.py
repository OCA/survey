# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _get_partner_nodes(self):
        """The questions opening a contact of their own.

        Filling in the name opens a contact, and then `survey_question_node_id`
        tells which contact it hangs from. Any other question fills in a field
        of the contact its own `survey_question_node_id` opened. A name answered
        outside any node belongs to the main generated contact instead.
        """
        self.ensure_one()
        questions = self.survey_id.question_ids
        nodes = questions.survey_question_node_id
        return questions.filtered(
            lambda x: x.res_partner_field.name == "name"
            and (x.survey_question_node_id or x in nodes)
        )

    def _get_partner_groups(self):
        """The answers that fill in a contact, grouped by the contact they fill"""
        self.ensure_one()
        nodes = self._get_partner_nodes()
        return self.user_input_line_ids.filtered(
            lambda x: x.question_id.res_partner_field and not x.skipped
        ).grouped(
            lambda x: x.question_id
            if x.question_id in nodes
            else x.question_id.survey_question_node_id
        )

    def _get_partner_node_children(self, groups, node):
        """The nodes whose contact hangs from the given node's one"""
        return [
            child
            for child in groups
            # A node whose own node answered nothing hangs from the main contact
            if child
            and (
                child.survey_question_node_id == node
                or (not node and child.survey_question_node_id not in groups)
            )
        ]

    def _prepare_partner(self):
        """Extract the values of the main contact from the answers"""
        self.ensure_one()
        groups = self._get_partner_groups()
        vals = self._prepare_partner_vals(
            groups.get(self.env["survey.question"], self.env["survey.user_input.line"])
        )
        vals["generating_survey_user_input_id"] = self.id
        return vals

    def _create_partner_nodes(self, groups, node, parent):
        """Generate the contact of every node hanging from the given one.

        `res.partner` sets `_allow_sudo_commands = False`, so the contacts can't
        be nested in the `child_ids` of their parent: the commands would run
        back as the survey taker, who isn't allowed to create contacts. Each
        contact gets its own `create()` instead, linked through `parent_id`.

        Returns the contacts generated right below the given node.
        """
        self.ensure_one()
        partners = self.env["res.partner"]
        for child in self._get_partner_node_children(groups, node):
            vals = self._prepare_partner_vals(groups[child])
            if not vals.get("name"):
                # A node whose name went unanswered opens no contact, so
                # whatever hangs from it hangs from its own node instead. Its
                # remaining answers are dropped: they have no contact to fill.
                partners |= self._create_partner_nodes(groups, child, parent)
                continue
            if parent:
                vals["parent_id"] = parent.id
            # `contact` children share their address with their parent, so a
            # node holding an address of its own needs a different type
            if child.res_partner_type:
                vals["type"] = child.res_partner_type
            partner = self.env["res.partner"].sudo().create(vals)
            self._create_contact_post_process(partner)
            self._create_partner_nodes(groups, child, partner)
            partners |= partner
        return partners

    def _prepare_partner_vals(self, elegible_inputs):
        """Extract the values of a single contact out of its group of answers"""
        self.ensure_one()
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
                vals[field_name] = (
                    line.suggested_answer_id.res_partner_field_resource_ref.id
                )
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
                        .sudo()
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
            partner = self.env["res.partner"]
            # Every answer may live inside a node, and then there's no main
            # contact to generate: the root node contact takes its place
            if set(vals) - {"generating_survey_user_input_id"}:
                email = vals.get("email")
                if email:
                    partner = user_input._get_existing_partner(email)
                if not partner:
                    partner = self.env["res.partner"].sudo().create(vals)
                    user_input._create_contact_post_process(partner)
            # The node contacts hang from the main one, when there's one
            roots = user_input._create_partner_nodes(
                user_input._get_partner_groups(), self.env["survey.question"], partner
            )
            if not partner:
                partner = next(iter(roots)) if len(roots) > 1 else roots
                partner.sudo().generating_survey_user_input_id = user_input
            if partner:
                user_input.update({"partner_id": partner.id, "email": partner.email})
        return super()._mark_done()
