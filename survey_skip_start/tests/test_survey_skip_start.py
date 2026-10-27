# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import HttpCase, tagged


@tagged("-at_install", "post_install")
class SurveySkipStartCase(HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.survey = self.env.ref("survey.survey_feedback")

    def test_skip_survey_start_screen(self):
        """Skip the start screen"""
        self.survey.skip_start = True
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_skip_start",
            step_delay=1000,
        )
