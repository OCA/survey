# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models
from odoo.tools import plaintext2html


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    sale_order_id = fields.Many2one(comodel_name="sale.order")

    def _prepare_quotation(self):
        return {
            "partner_id": self.create_uid.partner_id.id,
            "origin": self.survey_id.title,
            "survey_user_input_id": self.id,
            "company_id": self.create_uid.company_id.id,
            "team_id": self.survey_id.crm_team_id.id,
        }

    def _prepare_quotation_line(self, input_line):
        if input_line.question_id.question_type == "numerical_box":
            product_id = input_line.question_id.product_id
            qty = input_line.value_number
        else:
            product_id = input_line.value_suggested.product_id
            qty = 1
        return {
            "product_id": product_id.id,
            "product_uom_qty": qty,
        }

    def _prepare_quotation_comment(self):
        """We can have surveys without partner. It's handy to have some relevant info
        in the initial internal message for the salesmen to complete.

        :return str: comment for the quotation internal message
        """
        relevant_answers = self.user_input_line_ids.filtered(
            lambda x: not x.skipped and x.question_id.show_in_sale_order_comment
        )
        comment = "\n".join(
            f"{answer.question_id.title}: {answer[f'value_{answer.answer_type}']}"
            for answer in relevant_answers
        )
        return comment

    def _create_quotation_post_process(self):
        """After creating the quotation send an internal message with practical info"""
        message = _(
            "This order has been created from this survey input: "
            "<a href=# data-oe-model=survey.user_input data-oe-id=%d>%s</a>"
        ) % (self.id, self.survey_id.title)
        additional_comment = self._prepare_quotation_comment()
        if additional_comment:
            message += (
                f"<p>{_('Relevant answer informations:')}</p>"
                f"<p>{plaintext2html(additional_comment)}</p>"
            )
        self.sale_order_id.message_post(body=message)

    def _mark_done(self):
        """Generate the sale order when the survey is submitted"""
        res = super()._mark_done()
        if not self.survey_id.generate_quotations:
            return res
        quotable_lines = self.user_input_line_ids.filtered("value_suggested.product_id")
        quotable_lines += self.user_input_line_ids.filtered(
            lambda x: x.question_id.product_id and not x.skipped
        )
        if not quotable_lines:
            return res
        vals = self._prepare_quotation()
        vals["order_line"] = [
            (0, 0, self._prepare_quotation_line(line)) for line in quotable_lines
        ]
        self.sale_order_id = self.env["sale.order"].sudo().create(vals)
        self._create_quotation_post_process()
        return res
