# Copyright 2025 Binhex - Adasat Torres de Leon
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64

from odoo.modules.module import get_module_resource

from odoo.addons.survey.tests import common


class TestSurvey(common.SurveyCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, lang="en_US"))
        User = cls.env["res.users"].with_context(no_reset_password=True)
        (group_survey_manager, group_employee) = (
            cls.env.ref("survey.group_survey_manager").id,
            cls.env.ref("base.group_user").id,
        )

        cls.manager = User.create(
            {
                "name": "Manager",
                "login": "manager",
                "email": "manager@test.com",
                "groups_id": [(6, 0, [group_survey_manager, group_employee])],
            }
        )

        cls.survey1 = (
            cls.env["survey.survey"]
            .with_user(cls.manager)
            .create(
                {
                    "title": "Survey with signature",
                    "page_ids": [(0, 0, {"title": "Page0"})],
                }
            )
        )

        cls.page1 = (
            cls.env["survey.question"]
            .with_user(cls.manager)
            .create(
                {
                    "title": "Page1",
                    "survey_id": cls.survey1.id,
                    "sequence": 1,
                    "is_page": True,
                }
            )
        )

        cls.user_input1 = (
            cls.env["survey.user_input"]
            .with_user(cls.manager)
            .create(
                {
                    "survey_id": cls.survey1.id,
                    "partner_id": cls.manager.partner_id.id,
                }
            )
        )

        cls.question_signature = (
            cls.env["survey.question"]
            .with_user(cls.manager)
            .create(
                {
                    "title": "Signature",
                    "page_id": cls.page1.id,
                    "question_type": "signature",
                    "sequence": 2,
                    "constr_mandatory": True,
                    "constr_error_msg": "Signature is required.",
                }
            )
        )

        signature_path = get_module_resource(
            "survey_signature", "static", "src", "img", "signature.png"
        )

        with open(signature_path, "rb") as f:
            cls.signature_image = base64.b64encode(f.read())

    def test01_validate_signature(self):
        self.assertEqual(
            self.question_signature.validate_question(answer=False),
            {self.question_signature.id: self.question_signature.constr_error_msg},
        )
        self.assertEqual(
            self.question_signature.validate_question(answer=b""),
            {self.question_signature.id: self.question_signature.constr_error_msg},
        )

        self.assertEqual(
            self.question_signature.validate_question(answer=self.signature_image),
            {},
        )

    def test02_save_lines_signature(self):
        self.user_input1.save_lines(self.question_signature, self.signature_image)
        line = self.env["survey.user_input.line"].search(
            [
                ("user_input_id", "=", self.user_input1.id),
                ("question_id", "=", self.question_signature.id),
            ]
        )
        self.assertEqual(line.value_signature, self.signature_image)
        self.assertEqual(line.answer_type, "signature")
        self.assertEqual(line.display_name, "Signed")
