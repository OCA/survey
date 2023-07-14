# Copyright 2023 Jose Zambudio - Aures Tic <jose@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# from odoo.exceptions import ValidationError
import base64

from odoo.modules.module import get_module_resource

from odoo.addons.survey.tests import common


class TestSurvey(common.SurveyCase):
    def setUp(self):
        super(TestSurvey, self).setUp()
        User = self.env["res.users"].with_context({"no_reset_password": True})
        (group_survey_user, group_employee) = (
            self.ref("survey.group_survey_user"),
            self.ref("base.group_user"),
        )
        self.survey_manager = User.create(
            {
                "name": "Maria Riera",
                "login": "Riera",
                "email": "maria.riera@example.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.ref("survey.group_survey_manager"),
                            group_survey_user,
                            group_employee,
                        ],
                    )
                ],
            }
        )
        self.survey1 = (
            self.env["survey.survey"]
            .with_user(self.survey_manager)
            .create({"title": "S0", "page_ids": [(0, 0, {"title": "P0"})]})
        )
        self.page1 = (
            self.env["survey.question"]
            .with_user(self.survey_manager)
            .create(
                {
                    "title": "First page",
                    "survey_id": self.survey1.id,
                    "sequence": 1,
                    "is_page": True,
                }
            )
        )
        self.user_input1 = (
            self.env["survey.user_input"]
            .with_user(self.survey_manager)
            .create(
                {
                    "survey_id": self.survey1.id,
                    "partner_id": self.survey_manager.partner_id.id,
                }
            )
        )
        self.question_binary = (
            self.env["survey.question"]
            .with_user(self.survey_manager)
            .create(
                {
                    "title": "Test Binary",
                    "page_id": self.page1.id,
                    "question_type": "binary",
                    "allowed_filemimetypes": "application/pdf",
                    "max_filesize": 1024,
                    "constr_mandatory": True,
                    "validation_required": True,
                }
            )
        )
        self.question_multi_binary = (
            self.env["survey.question"]
            .with_user(self.survey_manager)
            .create(
                {
                    "title": "Test Binary",
                    "page_id": self.page1.id,
                    "question_type": "binary",
                    "allowed_filemimetypes": "image/png",
                    "max_filesize": 2097152,
                    "validation_required": True,
                }
            )
        )
        module_icon = get_module_resource(
            "survey_question_type_binary", "static", "description", "icon.png"
        )
        with open(module_icon, "rb") as img:
            self.image_base64 = base64.b64encode(img.read())
        module_html = get_module_resource(
            "survey_question_type_binary", "static", "description", "index.html"
        )
        with open(module_html, "rb") as file:
            self.html = base64.b64encode(file.read())

    def test_01_question_binary_with_error_values(self):
        self.assertEqual(
            self.question_binary.validate_question({}),
            {self.question_binary.id: self.question_binary.constr_error_msg},
        )
        self.assertEqual(
            self.question_binary.validate_question({"data": b""}),
            {self.question_binary.id: self.question_binary.constr_error_msg},
        )
        self.assertEqual(
            self.question_binary.validate_question({"data": "This is not a file"}),
            {self.question_binary.id: "This is not a file"},
        )
        self.assertEqual(
            self.question_binary.validate_question({"data": self.image_base64}),
            {
                self.question_binary.id: "The file cannot exceed {}MB in size.".format(
                    1 / 1024
                )
            },
        )
        self.question_binary.max_filesize = 2097152  # Increse to 2.0MB
        self.assertEqual(
            self.question_binary.validate_question({"data": self.image_base64}),
            {
                self.question_binary.id: "Only files with {} mime types are allowed.".format(
                    "application/pdf"
                )
            },
        )

    def test_02_question_binary_with_valid_values(self):
        self.question_binary.max_filesize = 2097152  # Increse to 2.0MB
        self.question_binary.allowed_filemimetypes = "image/png"
        self.assertEqual(
            self.question_binary.validate_question({"data": self.image_base64}),
            {},
        )
        self.user_input1.save_lines(
            question=self.question_binary,
            answer={
                "data": self.image_base64,
                "filename": "test image.png",
            },
        )
        self.assertTrue(
            self.user_input1.user_input_line_ids.filtered(
                lambda r: r.question_id == self.question_binary
            ).answer_binary_ids,
        )

    def test_03_question_multi_binary_with_valid_values(self):
        self.assertEqual(
            self.question_multi_binary.validate_question(
                [
                    {"data": self.image_base64},
                    {"data": self.image_base64},
                    {"data": self.image_base64},
                    {"data": self.image_base64},
                ]
            ),
            {},
        )

    def test_04_question_binary_data(self):
        self.user_input1.save_lines(
            question=self.question_multi_binary,
            answer=[
                {
                    "data": self.image_base64,
                    "filename": "test image.png",
                }
            ],
        )
        answer = self.user_input1.user_input_line_ids.filtered(
            lambda r: r.question_id == self.question_multi_binary
        ).answer_binary_ids
        self.assertTrue(
            answer.is_binary_image,
        )
        self.assertEqual(answer.value_binary_type, "image/png")
        self.assertEqual(answer.value_binary_size, 9455)
