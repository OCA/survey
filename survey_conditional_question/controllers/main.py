##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

import logging
from odoo.addons.survey.controllers.main import WebsiteSurvey
from odoo import http
from odoo.http import request


_logger = logging.getLogger(__name__)


class SurveyConditional(WebsiteSurvey):

    # TODO deberiamos heredar esto correctamente
    @http.route()
    def fill_survey(self, survey, token, prev=None, **post):
        '''Display and validates a survey'''
        Survey = request.env['survey.survey']
        UserInput = request.env['survey.user_input']

        # Controls if the survey can be displayed
        errpage = self._check_bad_cases(survey)
        if errpage:
            return errpage

        # Load the user_input
        user_input = UserInput.sudo().search([('token', '=', token)], limit=1)
        if not user_input:  # Invalid token
            return request.render("website.403")

        # Do not display expired survey (even if some pages have already been
        # displayed -- There's a time for everything!)
        errpage = self._check_deadline(user_input)
        if errpage:
            return errpage

        # Select the right page
        if user_input.state == 'new':  # First page
            page, page_nr, last = Survey.next_page(
                user_input, 0, go_back=False)
            data = {'survey': survey, 'page': page,
                    'page_nr': page_nr, 'token': user_input.token}
            data['hide_question_ids'] = UserInput.get_list_questions(
                survey, user_input)
            if last:
                data.update({'last': True})
            return request.render('survey.survey', data)
        elif user_input.state == 'done':  # Display success message
            return request.render(
                'survey.sfinished',
                {'survey': survey, 'token': token, 'user_input': user_input})
        elif user_input.state == 'skip':
            flag = (True if prev and prev == 'prev' else False)
            page, page_nr, last = Survey.next_page(
                user_input, user_input.last_displayed_page_id.id, go_back=flag)

            # special case if you click "previous" from the last page,
            # then leave the survey, then reopen it from the URL, avoid crash
            if not page:
                page, page_nr, last = Survey.next_page(
                    user_input, user_input.last_displayed_page_id.id,
                    go_back=True)

            data = {'survey': survey, 'page': page,
                    'page_nr': page_nr, 'token': user_input.token}
            if last:
                data.update({'last': True})
            data['hide_question_ids'] = UserInput.get_list_questions(
                survey, user_input)
            return request.render('survey.survey', data)
        else:
            return request.render("website.403")
