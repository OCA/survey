import io
import os
import zipfile
from base64 import b64encode

from odoo.modules.module import get_module_resource

from odoo.addons.survey.tests.common import TestSurveyCommon


class TestCertificationPy3o(TestSurveyCommon):
    def test_certification_py3o(self):
        demo_odt_path = get_module_resource(
            "survey_certification_py3o", "demo", "demo_report_certification.odt"
        )
        self.assertTrue(os.path.isfile(demo_odt_path))
        with open(demo_odt_path, "rb") as f:
            odt_data = f.read()
            try:
                zipfile.ZipFile(io.BytesIO(odt_data)).testzip()
            except zipfile.BadZipFile:
                self.fail("El archivo .odt no es válido (no es un ZIP correcto)")

        py3o_template = self.env["py3o.template"].create(
            {
                "name": "Demo Report Certification Template",
                "py3o_template_data": b64encode(odt_data),
                "filetype": "odt",
            }
        )
        test_certification = self.env["survey.survey"].create(
            {
                "title": "Test Certification py3o",
                "access_mode": "public",
                "users_login_required": True,
                "questions_layout": "page_per_question",
                "users_can_go_back": True,
                "scoring_type": "scoring_with_answers",
                "scoring_success_min": 85.0,
                "certification": True,
                "certification_mail_template_id": self.env.ref(
                    "survey.mail_template_certification"
                ).id,
                "is_time_limited": True,
                "time_limit": 10,
                "py3o_template_id": py3o_template.id,
            }
        )
        q_01 = self._add_question(
            None,
            "2+2",
            "simple_choice",
            sequence=1,
            constr_mandatory=True,
            constr_error_msg="Please select an answer",
            survey_id=test_certification.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4", "is_correct": True, "answer_score": 50.0},
                {"value": "5"},
            ],
        )
        q_02 = self._add_question(
            None,
            "2x2",
            "simple_choice",
            sequence=2,
            constr_mandatory=True,
            constr_error_msg="Please select an answer",
            survey_id=test_certification.id,
            labels=[
                {"value": "2"},
                {"value": "3"},
                {"value": "4", "is_correct": True, "answer_score": 50.0},
                {"value": "5"},
            ],
        )
        answer = self._add_answer(test_certification, self.env.user)
        self._add_answer_line(q_01, answer, q_01.suggested_answer_ids[2].id)
        self._add_answer_line(q_02, answer, q_02.suggested_answer_ids[2].id)
        answer.with_user(self.env.user).write({"state": "done"})
        answer._mark_done()
        self.assertEqual(
            answer.py3o_template_id.id, test_certification.py3o_template_id.id
        )
        report = self.env.ref(
            "survey_certification_py3o.custom_certification_report"
        ).with_user(self.env.uid)
        pdf_data = report._render_py3o([answer.id], data={"report_type": "pdf"})[0]
        self.assertTrue(pdf_data)
        self.assertIsInstance(pdf_data, bytes)
