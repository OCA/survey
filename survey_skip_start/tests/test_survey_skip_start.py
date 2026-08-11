# Copyright 2024 Tecnativa - David Vidal
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import HttpCase, tagged


@tagged("-at_install", "post_install")
class SurveySkipStartCase(HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.survey = self.env["survey.survey"].create(
            {
                "title": "Survey Test",
                "description": "A description test",
                "questions_layout": "page_per_section",
                "skip_start": True,
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

    def test_skip_survey_start_screen(self):
        """Skip the start screen"""
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_skip_start",
        )
