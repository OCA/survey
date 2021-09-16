##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

import json
import logging

from odoo import http
from odoo.http import request

from odoo.addons.survey.controllers.main import WebsiteSurvey

_logger = logging.getLogger(__name__)


class SurveyConditional(WebsiteSurvey):
    @http.route(
        [
            '/survey/hidden/<model("survey.survey"):survey>/<string:token>'
            "/<int:stored>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def hidden(self, survey, token, stored, **post):
        """ Pass the lists of hidden questions and pages to be applied in the
        Javascript.
        :param stored: indicate if we can rely on stored answers from a
        completed survey, or if we have to determine the hidden questions from
        the answers filled in so far. """
        ret = {"hidden_pages": [], "hidden_questions": []}
        user_input = (
            request.env["survey.user_input"].sudo().search([("token", "=", token)])
        )
        if stored:
            questions = user_input.user_input_line_ids.filtered("hidden").mapped(
                "question_id"
            )
        else:
            questions = user_input.get_hidden_questions()
        for question in questions:
            question_tag = "{}_{}_{}".format(
                question.survey_id.id,
                question.page_id.id,
                question.id,
            )
            ret["hidden_questions"].append(question_tag)
        for page in questions.mapped("page_id"):
            if not page.question_ids - questions:
                ret["hidden_pages"].append(page.id)
        return json.dumps(ret)
