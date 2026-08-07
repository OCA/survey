# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, new_test_user, tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("-at_install", "post_install")
class TestSurveyModelSelection(BaseCommon, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "partner test survey"})
        cls.user_portal = cls._create_new_portal_user(
            partner_id=cls.partner.id,
            login="portal_survey",
            password="portal_survey",
        )
        cls.survey = cls.env["survey.survey"].create(
            {
                "title": "Test Question Model",
                "survey_type": "custom",
                "questions_layout": "one_page",
                "access_mode": "public",
                "access_token": "b137640d-14d4-4748-9ef6-344caaaaaaf",
            }
        )
        cls.question = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "State",
                "question_type": "model",
                "question_model_id": cls.env["ir.model"]._get_id("res.country.state"),
                "question_domain": '[("country_id.name", "=", "Spain")]',
            }
        )

    def test_question_model(self):
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_question_model",
            login="portal_survey",
        )
        self.assertTrue(self.survey.user_input_ids.user_input_line_ids)

    def test_question_model_survey_manager_without_access_rights(self):
        """A survey editor is not necessarily an access rights administrator,
        but still needs to read ir.model to configure this question type."""
        survey_manager = new_test_user(
            self.env,
            login="survey_manager",
            groups="base.group_user,survey.group_survey_manager",
        )
        self.assertFalse(
            survey_manager.has_group("base.group_erp_manager"),
            "This test is only meaningful without access rights administration",
        )
        question = self.question.with_user(survey_manager)
        self.assertEqual(question.question_model_name, "res.country.state")
        # Creating a question of this type must not require ir.model write access
        question.copy()
