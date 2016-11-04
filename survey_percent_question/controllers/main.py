# -*- coding: utf-8 -*-
# Copyright 2015 Savoir-faire Linux
# Copyright 2016 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import json

from openerp import http
from openerp import SUPERUSER_ID
from openerp.http import request

from openerp.addons.survey.controllers.main import (
    WebsiteSurvey,
    dict_soft_update,
)

_logger = logging.getLogger(__name__)


class BaseWebsiteSurvey(WebsiteSurvey):
    # AJAX prefilling of a survey
    @http.route(['/survey/prefill/<model("survey.survey"):survey>/<string:token>',  # noqa
                 '/survey/prefill/<model("survey.survey"):survey>/<string:token>/<model("survey.page"):page>'],  # noqa
                type='http', auth='public', website=True)
    def prefill(self, survey, token, page=None, **post):
        cr, uid, context = request.cr, request.uid, request.context
        user_input_line_obj = request.registry['survey.user_input_line']
        ret = {}

        # Fetch previous answers
        if page:
            ids = user_input_line_obj.search(
                cr, SUPERUSER_ID, [('user_input_id.token', '=', token),
                                   ('page_id', '=', page.id)],
                context=context)
        else:
            ids = user_input_line_obj.search(
                cr, SUPERUSER_ID, [('user_input_id.token', '=', token)],
                context=context)
        previous_answers = user_input_line_obj.browse(cr, uid, ids,
                                                      context=context)

        # Return non empty answers in a JSON compatible format
        for answer in previous_answers:
            if not answer.skipped:
                answer_tag = '%s_%s_%s' % (
                    answer.survey_id.id,
                    answer.page_id.id,
                    answer.question_id.id,
                )
                answer_value = None
                if answer.answer_type == 'free_text':
                    answer_value = answer.value_free_text
                elif (answer.answer_type == 'text' and
                      answer.question_id.type == 'textbox'):
                    answer_value = answer.value_text
                elif (answer.answer_type == 'text' and
                      answer.question_id.type != 'textbox'):
                    # here come comment answers for matrices, simple choice and
                    # multiple choice
                    answer_tag = "%s_%s" % (answer_tag, 'comment')
                    answer_value = answer.value_text
                elif answer.question_id.type == 'percent_split':
                    if answer.value_suggested_row:
                        answer_tag = "%s_%s" % (answer_tag,
                                                answer.value_suggested_row.id)
                        answer_value = str(answer.value_number)
                    else:
                        dict_soft_update(ret,
                                         "%s_comment_label" % (answer_tag, ),
                                         answer.value_text)
                        answer_tag = "%s_comment_value" % (answer_tag, )
                        answer_value = str(answer.value_number)
                elif answer.answer_type == 'number':
                    answer_value = answer.value_number.__str__()
                elif answer.answer_type == 'date':
                    answer_value = answer.value_date
                elif (answer.answer_type == 'suggestion' and
                      not answer.value_suggested_row):
                    answer_value = answer.value_suggested.id
                elif (answer.answer_type == 'suggestion' and
                      answer.value_suggested_row):
                    answer_tag = "%s_%s" % (answer_tag,
                                            answer.value_suggested_row.id)
                    answer_value = answer.value_suggested.id
                if answer_value:
                    dict_soft_update(ret, answer_tag, answer_value)
                else:
                    _logger.warning(
                        "[survey] No answer has been found for question %s "
                        "marked as non skipped",
                        answer_tag)
        return json.dumps(ret)
