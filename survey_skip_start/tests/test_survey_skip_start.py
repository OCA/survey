# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import UserError
from odoo.tests import HttpCase, tagged


@tagged("-at_install", "post_install")
class SurveySkipStartCase(HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.survey = self.env.ref("survey.survey_feedback")
        self.survey.questions_layout = "page_per_section"

    def test_dont_skip_survey_start_screen(self):
        """Test the default behavior"""
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_dont_skip_start",
        )

    def test_skip_survey_start_screen(self):
        """Skip the start screen"""
        self.survey.questions_layout = "one_page"
        self.survey.skip_start = True
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_skip_start",
        )

    def test_skip_survey_start_screen_constraints(self):
        self.survey.questions_layout = "page_per_section"
        with self.assertRaises(UserError):
            self.survey.skip_start = True
