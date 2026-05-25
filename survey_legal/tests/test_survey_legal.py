# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import HttpCase, tagged


@tagged("-at_install", "post_install")
class SurveyLegalCase(HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.survey = self.env.ref("survey.survey_feedback")

    def test_survey_accept_legal_terms(self):
        self.survey.legal_terms = True
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_legal",
            step_delay=1000,
        )
        survey_question = self.env["survey.question"].search(
            [("title", "=", "Where do you live?")]
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
