import base64

from odoo.modules.module import get_module_resource
from odoo.tests.common import tagged

from odoo.addons.survey.tests import common


@tagged("-at_install", "post_install")
class TestSurveyCertificationBranding(common.TestSurveyCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        module_icon = get_module_resource(
            "survey_certification_branding", "static", "description", "icon.png"
        )
        with open(module_icon, "rb") as img:
            cls.certification_logo = base64.b64encode(img.read()).decode("utf-8")

        cls.certification_company_name = "Custom Company"

    def _assert_report_rendering(self, user_input):
        report = self.env.ref("survey.certification_report")
        res = str(report._render_qweb_html(report.id, user_input.ids)[0])
        certification = user_input.survey_id
        if certification.certification:
            self.assertIn(self.certification_company_name, res)
            self.assertIn("certification_logo_512", res)
        else:
            self.assertNotIn(self.certification_company_name, res)
            self.assertNotIn("certification_logo_512", res)

    def test_branding_fields_flow_and_certification_report_rendering(self):
        with self.with_user("survey_user"):
            certification = self.env["survey.survey"].create(
                {
                    "title": "Certification Branding",
                    "certification": True,
                    "certification_company_name": self.certification_company_name,
                    "certification_logo_512": self.certification_logo,
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

        # test certification branding fields
        self.assertEqual(
            certification.certification_company_name,
            self.certification_company_name,
        )

        self.assertEqual(
            certification.certification_logo_512.decode("utf-8"),
            self.certification_logo,
        )

        # test modern certification branding report rendering
        self._assert_report_rendering(user_input)

        # test classic certification branding report rendering
        certification.certification_report_layout = "classic_purple"
        self._assert_report_rendering(user_input)

        # test certification branding clearing
        certification.certification = False
        self.assertFalse(certification.certification_company_name)
        self.assertFalse(certification.certification_logo_512)
        # test classic certification built-in report rendering
        self._assert_report_rendering(user_input)

        # test modern certification built-in report rendering
        certification.certification_report_layout = "modern_purple"
        self._assert_report_rendering(user_input)
