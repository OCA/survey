from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestSurveyUserInputEditTour(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.survey = cls.env["survey.survey"].create(
            {
                "title": "Tour Feedback Survey",
                "access_token": "test_survey_user_input_edit_token",
                "access_mode": "public",
                "allow_editing": True,
                "questions_layout": "one_page",
            }
        )
        cls.question = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Feedback",
                "question_type": "char_box",
                "sequence": 1,
            }
        )

    def test_survey_user_input_edit_tour(self):
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_user_input_edit",
        )
