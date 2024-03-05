# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import datetime
from collections import defaultdict

from odoo import _, models


class Iterator:
    def __init__(self, value=0):
        self.value = value

    def next(self):
        self.value += 1
        return self.value


class ReportSurveyXlsx(models.AbstractModel):
    _name = "report.survey.xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "XLSX Report to show all the results for the survey"

    def _pre_generate_xlsx_report_header(self, sheet, results, cols, bold):
        # Hook for adding some extra headers at the beginning
        sheet.write(0, cols["partner_id"], _("Partner"), bold)
        sheet.write(0, cols["create_date"], _("Created on"), bold)

    def _post_generate_xlsx_report_header(self, sheet, results, cols, bold):
        # Hook for adding some extra headers at the end
        pass

    def _add_extra_data(self, user_input_data, user_input, cols):
        # Hook for adding extra data if needed
        for fieldname, col in cols.items():
            if fieldname in user_input._fields:
                if not isinstance(user_input[fieldname], models.Model):
                    user_input_data[col] = [user_input[fieldname]]
                elif user_input[fieldname]:
                    user_input_data[col] = [user_input[fieldname].display_name]

    def generate_xlsx_report(self, workbook, data, results):
        n_cols = Iterator(-1)
        sheet = workbook.add_worksheet("Survey Results")
        bold = workbook.add_format({"bold": True})
        no_bold = workbook.add_format({"bold": False})
        cols = defaultdict(n_cols.next)
        data = defaultdict(lambda: defaultdict(list))
        self._pre_generate_xlsx_report_header(sheet, results, cols, bold)
        # One column by question
        for question in results.question_ids:
            sheet.write(0, cols["question_%s" % question.id], question.title, bold)
        self._post_generate_xlsx_report_header(sheet, results, n_cols, bold)
        user_inputs = self.env["survey.user_input"].search(
            self._get_input_domain(results)
        )
        for user_input in user_inputs:
            self._add_extra_data(data[user_input.id], user_input, cols)
            for user_answer in user_input.user_input_line_ids:
                question_id = "question_%s" % user_answer.question_id.id
                if question_id not in cols or user_answer.skipped:
                    # We should ignore old removed questions
                    continue
                data[user_input.id][cols[question_id]].append(
                    user_answer._get_xlsx_value()
                )
        row = 0
        for answer_data in data.values():
            row += 1
            for col_id, answer_vals in answer_data.items():
                if isinstance(answer_vals[0], datetime.datetime):
                    date = answer_vals[0].date()
                    answer_vals[0] = date.isoformat()
                result = (
                    answer_vals[0] if len(answer_vals) == 1 else ", ".join(answer_vals)
                )
                sheet.write(
                    row,
                    col_id,
                    result,
                    no_bold,
                )

    def _get_input_domain(self, results):
        return [
            ("survey_id", "=", results.id),
            ("test_entry", "=", False),
            ("state", "=", "done"),
        ]
