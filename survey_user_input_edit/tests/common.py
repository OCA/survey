from odoo.tests.common import TransactionCase


class TestSurveyUserInputEditCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = cls.env["survey.survey"].create(
            {
                "title": "Feedback Survey",
                "allow_editing": True,
                "questions_layout": "page_per_question",
                "access_mode": "public",
            }
        )
        cls.question_1 = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Feedback text",
                "question_type": "char_box",
                "sequence": 1,
            }
        )
        cls.question_2 = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Additional comments",
                "question_type": "text_box",
                "sequence": 2,
            }
        )
        cls.user_input = cls.env["survey.user_input"].create(
            {
                "survey_id": cls.survey.id,
                "partner_id": cls.env.user.partner_id.id,
                "email": cls.env.user.email,
                "state": "done",
                "predefined_question_ids": [
                    (6, 0, (cls.question_1 | cls.question_2).ids)
                ],
            }
        )
