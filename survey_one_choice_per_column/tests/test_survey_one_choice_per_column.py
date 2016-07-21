# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestSurveyOneChoicePerColumn(TransactionCase):

    def setUp(self):
        super(TestSurveyOneChoicePerColumn, self).setUp()
        self.survey_obj = self.env['survey.survey']
        self.survey_page_obj = self.env['survey.page']
        self.question_obj = self.env['survey.question']
        label_obj = self.env['survey.label']
        self.survey = self.survey_obj.create({'title': 'Test Survey'})
        self.page = self.survey_page_obj.create({'title': 'Test Page',
                                                 'survey_id': self.survey.id
                                                 })
        subtype = 'simple_restricted'
        self.question = self.question_obj.create({'question': 'Test Question',
                                                  'type': 'matrix',
                                                  'page_id': self.page.id,
                                                  'matrix_subtype': subtype,
                                                  'constr_mandatory': True
                                                  })
        self.question2 = self.question_obj.create({'question': 'Tes Question2',
                                                   'type': 'textbox',
                                                   'page_id': self.page.id,
                                                   'constr_mandatory': False
                                                   })
        self.user_input_obj = self.env['survey.user_input']
        self.user_input_line_obj = self.env['survey.user_input_line']
        self.columns = []
        self.rows = []
        for i in range(4):
            column = label_obj.create({'question_id': self.question.id,
                                       'value': str(i),
                                       'sequence': i,
                                       'quizz_mark': float(i)
                                       })
            row = label_obj.create({'question_id_2': self.question.id,
                                    'value': str(i),
                                    'sequence': i,
                                    'quizz_mark': float(i)
                                    })
            self.columns.append(column)
            self.rows.append(row)

    def test_ideal(self):
        answer_tag = '%s_%s_%s' % (self.survey.id,
                                   self.page.id,
                                   self.question.id)
        post = {}
        for i in range(4):
            key = answer_tag + ('_%s' % self.rows[i].id)
            post[key] = self.columns[i].id
        res = self.question_obj.validate_question(self.question,
                                                  post,
                                                  answer_tag)
        self.assertEquals(len(res), 0)

    def test_multi_answers_for_column(self):
        answer_tag = '%s_%s_%s' % (self.survey.id,
                                   self.page.id,
                                   self.question.id)
        post = {}
        for i in range(4):
            key = answer_tag + ('_%s' % self.rows[i].id)
            post[key] = self.columns[0].id
        res = self.question_obj.validate_question(self.question,
                                                  post,
                                                  answer_tag)
        self.assertEquals(len(res), 1)

    def test_mandatory(self):
        answer_tag = '%s_%s_%s' % (self.survey.id,
                                   self.page.id,
                                   self.question.id)
        post = {}
        for i in range(3):
            key = answer_tag + ('_%s' % self.rows[i].id)
            post[key] = self.columns[i].id
        res = self.question_obj.validate_question(self.question,
                                                  post,
                                                  answer_tag)
        self.assertEquals(len(res), 1)

    def test_validation_not_obstructive(self):
        answer_tag = '%s_%s_%s' % (self.survey.id,
                                   self.page.id,
                                   self.question2.id)
        post = {
            answer_tag: 'Nothing'
        }
        res = self.question_obj.validate_question(self.question2,
                                                  post,
                                                  answer_tag)
        self.assertEquals(len(res), 0)

    def test_save_lines(self):
        self.question.write({'matrix_subtype': 'simple_restricted'})
        answer_tag = '%s_%s_%s' % (self.survey.id,
                                   self.page.id,
                                   self.question.id)
        post = {}
        for i in range(4):
            key = answer_tag + ('_%s' % self.rows[i].id)
            post[key] = self.columns[i].id
        input = self.user_input_obj.create({'survey_id': self.survey.id})
        res = self.user_input_line_obj.save_lines(input.id,
                                                  self.question,
                                                  post,
                                                  answer_tag)
        # custom method returns True
        self.assertTrue(res)

    def test_save_lines_not_obstructive(self):
        self.question.write({'matrix_subtype': 'simple'})
        answer_tag = '%s_%s_%s' % (self.survey.id,
                                   self.page.id,
                                   self.question.id)
        post = {}
        for i in range(4):
            key = answer_tag + ('_%s' % self.rows[i].id)
            post[key] = self.columns[i].id
        input = self.user_input_obj.create({'survey_id': self.survey.id})
        res = self.user_input_line_obj.save_lines(input.id,
                                                  self.question,
                                                  post,
                                                  answer_tag)
        # standard method does not return a value (None)
        self.assertEquals(res, None)

    def test_save_lines_no_answers(self):
        self.question.write({'matrix_subtype': 'simple_restricted'})
        answer_tag = '%s_%s_%s' % (self.survey.id,
                                   self.page.id,
                                   self.question.id)
        input = self.user_input_obj.create({'survey_id': self.survey.id})
        self.user_input_line_obj.save_lines(input.id,
                                            self.question,
                                            {},
                                            answer_tag)
        c = self.user_input_line_obj.search([('user_input_id', '=', input.id),
                                             ('skipped', '=', True)
                                             ])
        self.assertEquals(len(c), 1)
