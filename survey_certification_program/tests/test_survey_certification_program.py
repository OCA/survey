from odoo import _
from odoo.exceptions import ValidationError
from odoo.fields import Command
from odoo.tests.common import tagged

from odoo.addons.survey.tests import common


@tagged("-at_install", "post_install")
class TestSurveyCertificationProgram(common.TestSurveyCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.program_line1 = {
            "sequence": 1,
            "name": "Program Line 1",
            "description": "<p>Program Line 1 Description</p>",
            "hours": 1.0,
        }
        cls.program_line2 = {
            "sequence": 2,
            "name": "Program Line 2",
            "description": "<p>Program Line 2 Description</p>",
            "hours": 2.0,
        }

    def test_certification_program_lines_are_required(self):
        with self.with_user("survey_user"):
            with self.assertRaisesRegex(
                ValidationError,
                _(
                    "You must add at least one Certification Program Line before saving."
                ),
            ):
                self.env["survey.survey"].create(
                    {
                        "title": "Certification Test",
                        "certification": True,
                        "certification_program_enabled": True,
                        "certification_program_layout": "simple",
                        "access_mode": "public",
                        "users_login_required": True,
                        "questions_layout": "page_per_question",
                        "scoring_type": "scoring_with_answers",
                        "scoring_success_min": 1,
                    }
                )

    def _assert_report_rendering(self, user_input):
        report = self.env.ref("survey.certification_report")
        res = str(report._render_qweb_html(report.id, user_input.ids)[0])
        certification = user_input.survey_id
        if certification.certification_program_enabled:
            self.assertIn("Program Line 1", res)
            self.assertIn("Program Line 2", res)
        else:
            self.assertNotIn("Program Line 1", res)
            self.assertNotIn("Program Line 2", res)

    def test_program_table_flow_and_certification_report_rendering(self):
        with self.with_user("survey_user"):
            certification = self.env["survey.survey"].create(
                {
                    "title": "Certification Test",
                    "certification": True,
                    "certification_program_enabled": True,
                    "certificate_program_line_ids": [
                        Command.create(self.program_line1),
                        Command.create(self.program_line2),
                    ],
                    "certification_program_layout": "simple",
                    "access_mode": "public",
                    "users_login_required": True,
                    "questions_layout": "page_per_question",
                    "scoring_type": "scoring_with_answers",
                    "scoring_success_min": 1,
                }
            )

            q01 = self._add_question(
                None,
                "Q1",
                "simple_choice",
                sequence=1,
                constr_mandatory=True,
                constr_error_msg="Please select an answer",
                survey_id=certification.id,
                labels=[
                    {"value": "Wrong answer"},
                    {
                        "value": "Correct answer!!!",
                        "is_correct": True,
                        "answer_score": 2.0,
                    },
                ],
            )

        user_input = self._add_answer(certification, self.survey_user.partner_id)
        self._add_answer_line(
            q01,
            user_input,
            q01.suggested_answer_ids[-1]["id"],
        )

        user_input.state = "done"

        # test certification program simple report rendering
        self.assertEqual(
            certification.certification_program_layout,
            "simple",
        )
        self._assert_report_rendering(user_input)

        # test certification program columns report rendering
        certification.certification_program_layout = "columns"
        self.assertEqual(
            certification.certification_program_layout,
            "columns",
        )
        self._assert_report_rendering(user_input)
