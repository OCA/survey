# Copyright 2023 Jose Zambudio - Aures Tic <jose@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64

from odoo.exceptions import ValidationError
from odoo.tools.misc import file_path

from odoo.addons.survey.tests import common


class TestSurvey(common.SurveyCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = cls.env["res.users"].with_context(no_reset_password=True)
        (group_survey_user, group_employee) = (
            cls.env.ref("survey.group_survey_user").id,
            cls.env.ref("base.group_user").id,
        )
        cls.survey_manager = User.create(
            {
                "name": "Maria Riera",
                "login": "Riera",
                "email": "maria.riera@example.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            cls.env.ref("survey.group_survey_manager").id,
                            group_survey_user,
                            group_employee,
                        ],
                    )
                ],
            }
        )
        cls.survey1 = (
            cls.env["survey.survey"]
            .with_user(cls.survey_manager)
            .create({"title": "S0", "page_ids": [(0, 0, {"title": "P0"})]})
        )
        cls.page1 = (
            cls.env["survey.question"]
            .with_user(cls.survey_manager)
            .create(
                {
                    "title": "First page",
                    "survey_id": cls.survey1.id,
                    "sequence": 1,
                    "is_page": True,
                }
            )
        )
        cls.user_input1 = (
            cls.env["survey.user_input"]
            .with_user(cls.survey_manager)
            .create(
                {
                    "survey_id": cls.survey1.id,
                    "partner_id": cls.survey_manager.partner_id.id,
                }
            )
        )
        cls.question_binary = (
            cls.env["survey.question"]
            .with_user(cls.survey_manager)
            .create(
                {
                    "title": "Test Binary",
                    "page_id": cls.page1.id,
                    "question_type": "binary",
                    "allowed_filemimetypes": "application/pdf",
                    "max_filesize": 1024,
                    "constr_mandatory": True,
                    "validation_required": True,
                }
            )
        )
        cls.question_multi_binary = (
            cls.env["survey.question"]
            .with_user(cls.survey_manager)
            .create(
                {
                    "title": "Test Binary",
                    "page_id": cls.page1.id,
                    "question_type": "multi_binary",
                    "allowed_filemimetypes": "image/png",
                    "max_filesize": 2097152,
                    "validation_required": True,
                }
            )
        )
        with open(
            file_path("survey_question_type_binary/static/description/icon.png"), "rb"
        ) as img:
            cls.image_base64 = base64.b64encode(img.read())
        with open(
            file_path("survey_question_type_binary/static/description/index.html"),
            "rb",
        ) as f:
            cls.html = base64.b64encode(f.read())

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
            {self.question_binary.id: f"The file cannot exceed {1 / 1024}MB in size."},
        )
        self.question_binary.max_filesize = 2097152  # Increse to 2.0MB
        self.assertEqual(
            self.question_binary.validate_question({"data": self.image_base64}),
            {
                self.question_binary.id: (
                    "Only files with {} mime types are allowed.".format(
                        "application/pdf"
                    )
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
        self.user_input1._save_lines(
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
        self.user_input1._save_lines(
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

    def test_05_validate_question_non_binary(self):
        # covers: validate_question → super() for non-binary question types (line 32)
        q_char = self.env["survey.question"].create(
            {
                "title": "Text Question",
                "survey_id": self.survey1.id,
                "question_type": "char_box",
                "constr_mandatory": False,
            }
        )
        result = q_char.validate_question("some answer")
        self.assertEqual(result, {})

    def test_06_save_lines_non_binary(self):
        # covers: _save_lines → super() for non-binary question types (line 28)
        q_char = self.env["survey.question"].create(
            {
                "title": "Text Question 2",
                "survey_id": self.survey1.id,
                "question_type": "char_box",
            }
        )
        self.user_input1._save_lines(question=q_char, answer="hello")
        line = self.user_input1.user_input_line_ids.filtered(
            lambda r: r.question_id == q_char
        )
        self.assertEqual(line.value_char_box, "hello")

    def test_07_check_answer_type_skipped_empty_binary(self):
        # covers: _check_answer_type_skipped ValidationError when answer_binary_ids
        # is empty for a binary-type line
        with self.assertRaises(ValidationError):
            self.env["survey.user_input.line"].create(
                {
                    "user_input_id": self.user_input1.id,
                    "question_id": self.question_binary.id,
                    "answer_type": "binary",
                }
            )

    def test_08_check_binary_answer_max_filesize(self):
        # covers: _check_binary_answer ValidationError when file exceeds max_filesize
        # question_binary.max_filesize=1024 bytes; image is ~9455 bytes
        with self.assertRaises(ValidationError):
            self.env["survey.user_input.line"].create(
                {
                    "user_input_id": self.user_input1.id,
                    "question_id": self.question_binary.id,
                    "answer_type": "binary",
                    "answer_binary_ids": [
                        (
                            0,
                            0,
                            {
                                "value_binary": self.image_base64,
                                "filename": "test.png",
                            },
                        )
                    ],
                }
            )

    def test_09_check_binary_answer_mimetype(self):
        # covers: _check_binary_answer ValidationError when mimetype not allowed
        # question has large max_filesize so only the mimetype check fires
        q_pdf_only = self.env["survey.question"].create(
            {
                "title": "PDF Only Question",
                "survey_id": self.survey1.id,
                "question_type": "binary",
                "allowed_filemimetypes": "application/pdf",
                "max_filesize": 10485760,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["survey.user_input.line"].create(
                {
                    "user_input_id": self.user_input1.id,
                    "question_id": q_pdf_only.id,
                    "answer_type": "binary",
                    "answer_binary_ids": [
                        (
                            0,
                            0,
                            {
                                "value_binary": self.image_base64,
                                "filename": "test.png",
                            },
                        )
                    ],
                }
            )

    def test_10_compute_display_name(self):
        # covers: _compute_display_name for binary (shows filename),
        # multi_binary (shows file count), and non-binary (uses super display_name)
        q_char = self.env["survey.question"].create(
            {
                "title": "Char Question Display",
                "survey_id": self.survey1.id,
                "question_type": "char_box",
            }
        )
        self.user_input1._save_lines(question=q_char, answer="hello")
        char_line = self.user_input1.user_input_line_ids.filtered(
            lambda r: r.question_id == q_char
        )
        # Non-binary line: both ifs in _compute_display_name short-circuit to False
        self.assertTrue(char_line.display_name)

        q_bin = self.env["survey.question"].create(
            {
                "title": "Image Binary Question",
                "survey_id": self.survey1.id,
                "question_type": "binary",
                "allowed_filemimetypes": "image/png",
                "max_filesize": 10485760,
            }
        )
        self.user_input1._save_lines(
            question=q_bin,
            answer={"data": self.image_base64, "filename": "photo.png"},
        )
        binary_line = self.user_input1.user_input_line_ids.filtered(
            lambda r: r.question_id == q_bin
        )
        self.assertEqual(binary_line.display_name, "photo.png")

        self.user_input1._save_lines(
            question=self.question_multi_binary,
            answer=[
                {"data": self.image_base64, "filename": "a.png"},
                {"data": self.image_base64, "filename": "b.png"},
            ],
        )
        multi_line = self.user_input1.user_input_line_ids.filtered(
            lambda r: r.question_id == self.question_multi_binary
        )
        self.assertIn("2", multi_line.display_name)

    def test_11_save_lines_binary_empty_answer(self):
        # covers: if not answer: answer = [False] branch in _save_lines
        # and: if answer_type in (...) and answer: False in _get_line_answer_values
        q_bin = self.env["survey.question"].create(
            {
                "title": "Empty Binary Question",
                "survey_id": self.survey1.id,
                "question_type": "binary",
                "allowed_filemimetypes": "image/png",
                "max_filesize": 10485760,
            }
        )
        self.user_input1._save_lines(question=q_bin, answer=[])
        line = self.user_input1.user_input_line_ids.filtered(
            lambda r: r.question_id == q_bin
        )
        self.assertTrue(line.skipped)
