# -*- coding: utf-8 -*-
# © 2017 Sunflower IT (http://sunflowerweb.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class TestSurveyAnswerOnce(TransactionCase):
    def setUp(self):
        super(TestSurveyAnswerOnce, self).setUp()
        self.partner_obj = self.env["res.partner"]
        self.user_obj = self.env["res.users"]
        self.survey_obj = self.env['survey.survey']
        self.survey_page_obj = self.env['survey.page']
        self.question_obj = self.env['survey.question']
        self.survey = self.survey_obj.create({'title': 'Test Survey'})
        self.user = self.user_obj.create({
            'login': 'testtesttest',
            'name': 'Test Test'
        })
        self.page = self.survey_page_obj.create({
            'title': 'Test Page',
            'survey_id': self.survey.id
        })
        self.question = self.question_obj.create({
            'question': 'Test Question',
            'type': 'free_text',
            'page_id': self.page.id,
            'constr_mandatory': True
        })
        self.user_input_obj = self.env['survey.user_input']
        self.user_input_line_obj = self.env['survey.user_input_line']

    def test_try_to_answer_twice(self):
        self.survey.allow_duplicates = False
        answer_tag = '%s_%s_%s' % (
            self.survey.id,
            self.page.id,
            self.question.id
        )
        post = {answer_tag: 'Test answer'}
        iteration = 0
        try:
            for i in range(2):
                # created by admin
                _input = self.user_input_obj.create({
                    'survey_id': self.survey.id,
                    'partner_id': self.user.partner_id.id
                })
                # answered by test user
                self.user_input_line_obj.sudo(self.user.id).save_lines(
                    _input.id,
                    self.question,
                    post,
                    answer_tag
                )
                iteration += 1
        except ValidationError as e:
            self.assertEquals(e.args[1], 'duplicate_answer')
        # Second answer should have been disallowed by ValidationError
        self.assertEquals(iteration, 1)

        # Final result should be that only one answer was saved
        answers = self.env['survey.user_input_line'].search([
            ('question_id', '=', self.question.id),
            ('user_input_id.partner_id', '=', self.user.partner_id.id)
        ])
        self.assertEquals(len(answers), 1)
