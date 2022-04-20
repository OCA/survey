# Copyright 2022 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import date

import freezegun

from odoo.addons.survey.tests import common

_logger = logging.getLogger(__name__)

try:
    from xlrd import open_workbook
except ImportError:
    _logger.debug("Can not import xlrd`.")


@freezegun.freeze_time("2022-04-26")
class TestReport(common.TestSurveyCommon):
    def setUp(self):
        super(TestReport, self).setUp()
        self.question_date = (
            self.env["survey.question"]
            .with_user(self.survey_manager)
            .create(
                {
                    "title": "Test Date",
                    "survey_id": self.survey.id,
                    "sequence": 4,
                    "question_type": "date",
                }
            )
        )
        self.suggested_question = self._add_question(
            page=self.question_date.page_id,
            name="Test Suggested",
            qtype="simple_choice",
            labels=[
                {"value": "FIRST", "suggested_answer_id": True},
                {"value": "SECOND"},
            ],
            survey_id=self.survey.id,
            sequence=5,
        )

        answer = self._add_answer(self.survey, False, email="public@example.com")
        self._add_answer_line(self.question_ft, answer, "FIRST ANSWER")
        self._add_answer_line(self.question_num, answer, 1)
        self._add_answer_line(self.question_date, answer, date.today())
        self._add_answer_line(
            self.suggested_question,
            answer,
            self.suggested_question.suggested_answer_ids[0]["id"],
        )
        answer._mark_done()
        answer2 = self._add_answer(self.survey, False, email="public2@example.com")
        self._add_answer_line(self.question_ft, answer2, "SECOND ANSWER")
        self._add_answer_line(self.question_num, answer2, 2)
        self._add_answer_line(
            self.question_date, answer2, False, skipped=True, answer_type=False
        )
        self._add_answer_line(
            self.suggested_question,
            answer2,
            self.suggested_question.suggested_answer_ids[1]["id"],
        )
        answer2._mark_done()

    def test_report(self):
        report = self.env.ref("survey_xlsx.report_survey_xlsx")
        self.assertEqual(report.report_type, "xlsx")
        rep = report._render(self.survey.ids, {})
        wb = open_workbook(file_contents=rep[0])
        sheet = wb.sheet_by_index(0)

        self.assertEqual(sheet.cell(1, 2).value, "FIRST ANSWER")
        self.assertEqual(sheet.cell(2, 2).value, "SECOND ANSWER")
        self.assertEqual(sheet.cell(1, 3).value, 1)
        self.assertEqual(sheet.cell(2, 3).value, 2)
        self.assertEqual(sheet.cell(1, 4).value, "2022-04-26")
        self.assertFalse(sheet.cell(2, 4).value)
        self.assertEqual(sheet.cell(1, 5).value, "FIRST")
        self.assertEqual(sheet.cell(2, 5).value, "SECOND")
