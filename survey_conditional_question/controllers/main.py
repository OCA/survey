#############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
#############################################################################

import logging
from collections import defaultdict

from odoo.addons.survey.controllers.main import Survey

_logger = logging.getLogger(__name__)


class SurveyConditional(Survey):
    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        result = super(SurveyConditional, self)._prepare_survey_data(
            survey_sudo, answer_sudo, **post
        )
        if survey_sudo.questions_layout != "page_per_question":
            (
                _questions,
                triggered_questions_by_answer,
                _answers,
            ) = answer_sudo._get_conditional_values()
            no_answer_questions = triggered_questions_by_answer.get(
                answer_sudo.env["survey.question.answer"],
                answer_sudo.env["survey.question"],
            )
            no_answer_questions_by_question = defaultdict(lambda: [])

            for question in no_answer_questions:
                no_answer_questions_by_question[
                    question.triggering_question_id.id
                ].append(
                    [
                        question.id,
                        question.conditional_minimum_value,
                        question.conditional_maximum_value,
                    ]
                )
            result.update(
                {
                    "no_answer_conditional_questions": {
                        question.id: [
                            question.triggering_question_id,
                            question.conditional_minimum_value,
                            question.conditional_maximum_value,
                        ]
                        for question in no_answer_questions
                    },
                    "no_answer_conditional_questions_"
                    "by_question": no_answer_questions_by_question,
                }
            )
        return result
