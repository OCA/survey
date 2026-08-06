# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class SurveyLegalCase(HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.survey = self.env["survey.survey"].create(
            {
                "title": "Survey Test",
                "description": "A description test",
                "questions_layout": "page_per_section",
                "legal_terms": True,
                "question_and_page_ids": [
                    Command.create(
                        {"title": "Page Test", "is_page": True, "sequence": 1}
                    ),
                    Command.create(
                        {
                            "title": "Where do you live?",
                            "question_type": "char_box",
                            "is_page": False,
                            "sequence": 2,
                        }
                    ),
                ],
            }
        )

    def test_survey_accept_legal_terms(self):
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_legal",
        )
        survey_question = self.env["survey.question"].search(
            [("title", "=", "Where do you live?"), ("survey_id", "=", self.survey.id)]
        )
        self.assertTrue(
            self.env["survey.user_input.line"]
            .search(
                [
                    ("question_id", "=", survey_question.id),
                    ("value_char_box", "=", "Mordor-les-bains"),
                ]
            )
            .user_input_id.user_metadata
        )
