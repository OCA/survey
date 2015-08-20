# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tests import TransactionCase


class TestSurveyCalculator(TransactionCase):

    def setUp(self):

        super(TestSurveyCalculator, self).setUp()

        self.PartnerObj = self.env['res.partner']
        self.SurveyObj = self.env['survey.survey']
        self.SurveyPageObj = self.env['survey.page']
        self.SurveyQuestionObj = self.env['survey.question']
        self.SurveyLabelObj = self.env['survey.label']
        self.SurveyUserInputObj = self.env['survey.user_input']
        self.SurveyUserInputLineObj = self.env['survey.user_input_line']
        self.ComputationObj = self.env['survey.calculator.computation']
        self.ResultObj = self.env['survey.calculator.result']

        self.partner_company = self.PartnerObj.create({
            'name': 'Company Test',
            'is_company': True,
        })

        self.partner = self.PartnerObj.create({
            'name': 'Partner Test',
            'is_company': False,
            'parent_id': self.partner_company.id,
        })

        self.survey = self.SurveyObj.create({
            'title': 'Survey Test',
        })

        self.page = self.SurveyPageObj.create({
            'survey_id': self.survey.id,
            'title': 'Page Test',
        })

        self.questions = [
            self.SurveyQuestionObj.create({
                'page_id': self.page.id,
                'question': record[0],
                'type': record[1],
                'matrix_subtype': record[2],
            }) for record in [
                ('Why are you there?',                          # 0
                 'free_text', 'simple'),
                ('What is your favorite band?',                 # 1
                 'textbox', 'simple'),
                ('What is your favorite number?',               # 2
                 'numerical_box', 'simple'),
                ('What is your favorite date?',                 # 3
                 'datetime', 'simple'),
                ('What is your gender?',                        # 4
                 'simple_choice', 'simple'),
                ('What are your favorite colors?',              # 5
                 'multiple_choice', 'simple'),
                ('What color do you want for these objects?',   # 6
                 'matrix', 'simple'),
                ('What colors do you want for these objects?',  # 7
                 'matrix', 'multiple'),
            ]
        ]

        self.labels = [
            self.SurveyLabelObj.create({
                'question_id': record[0],
                'question_id_2': record[1],
                'value': record[2],
            }) for record in [
                (self.questions[4].id, False, 'Male'),       # 0
                (self.questions[4].id, False, 'Female'),     # 1
                (self.questions[4].id, False, 'Pineapple'),  # 2
                (self.questions[5].id, False, 'Red'),        # 3
                (self.questions[5].id, False, 'Green'),      # 4
                (self.questions[5].id, False, 'Yellow'),     # 5
                (False, self.questions[6].id, 'Table'),      # 6
                (False, self.questions[6].id, 'Chair'),      # 7
                (False, self.questions[6].id, 'Door'),       # 8
                (self.questions[6].id, False, 'Red'),        # 9
                (self.questions[6].id, False, 'Green'),      # 10
                (self.questions[6].id, False, 'Yellow'),     # 11
                (False, self.questions[7].id, 'Wall'),       # 12
                (False, self.questions[7].id, 'Desk'),       # 13
                (False, self.questions[7].id, 'Lamp'),       # 14
                (self.questions[7].id, False, 'Red'),        # 15
                (self.questions[7].id, False, 'Green'),      # 16
                (self.questions[7].id, False, 'Yellow'),     # 17
            ]
        ]

        self.user_inputs = [
            self.SurveyUserInputObj.create({
                'survey_id': self.survey.id,
                'state': 'done',
                'partner_id': self.partner.id,
            }) for i in range(3)
        ]

        self.user_input_lines = [
            self.SurveyUserInputLineObj.create({
                'user_input_id': record[0],
                'question_id': record[1],
                record[2]: record[3],
                'value_suggested_row': record[4],
                'answer_type': record[5],
            }) for record in [
                # User_input 0
                (self.user_inputs[0].id, self.questions[0].id,
                 'value_free_text', 'Why not?', False, 'free_text'),
                (self.user_inputs[0].id, self.questions[1].id,
                 'value_text', 'Spice Girls', False, 'text'),
                (self.user_inputs[0].id, self.questions[2].id,
                 'value_number', 4, False, 'number'),
                (self.user_inputs[0].id, self.questions[3].id,
                 'value_date', '2012-10-10 09:10:10', False, 'date'),
                (self.user_inputs[0].id, self.questions[4].id,  # Female
                 'value_suggested', self.labels[1].id, False, 'suggestion'),
                (self.user_inputs[0].id, self.questions[5].id,  # Red
                 'value_suggested', self.labels[3].id, False, 'suggestion'),
                (self.user_inputs[0].id, self.questions[5].id,  # Yellow
                 'value_suggested', self.labels[5].id, False, 'suggestion'),
                (self.user_inputs[0].id, self.questions[6].id,  # Table Red
                 'value_suggested', self.labels[9].id, self.labels[6].id,
                 'suggestion'),
                (self.user_inputs[0].id, self.questions[6].id,  # Chair Red
                 'value_suggested', self.labels[9].id, self.labels[7].id,
                 'suggestion'),
                (self.user_inputs[0].id, self.questions[6].id,  # Door Red
                 'value_suggested', self.labels[9].id, self.labels[8].id,
                 'suggestion'),
                (self.user_inputs[0].id, self.questions[7].id,  # Wall Green
                 'value_suggested', self.labels[16].id, self.labels[12].id,
                 'suggestion'),
                (self.user_inputs[0].id, self.questions[7].id,  # Wall Yellow
                 'value_suggested', self.labels[17].id, self.labels[12].id,
                 'suggestion'),
                (self.user_inputs[0].id, self.questions[7].id,  # Desk Red
                 'value_suggested', self.labels[15].id, self.labels[13].id,
                 'suggestion'),
                (self.user_inputs[0].id, self.questions[7].id,  # Desk Yellow
                 'value_suggested', self.labels[17].id, self.labels[13].id,
                 'suggestion'),
                (self.user_inputs[0].id, self.questions[7].id,  # Lamp Red
                 'value_suggested', self.labels[15].id, self.labels[14].id,
                 'suggestion'),

                # User_input 1
                (self.user_inputs[1].id, self.questions[0].id,
                 'value_free_text', 'I saw some light...', False, 'free_text'),
                (self.user_inputs[1].id, self.questions[1].id,
                 'value_text', 'Queen', False, 'text'),
                (self.user_inputs[1].id, self.questions[2].id,
                 'value_number', 12, False, 'number'),
                (self.user_inputs[1].id, self.questions[3].id,
                 'value_date', '2015-10-10 09:10:10', False, 'date'),
                (self.user_inputs[1].id, self.questions[4].id,  # Pineapple
                 'value_suggested', self.labels[3].id, False, 'suggestion'),
                (self.user_inputs[1].id, self.questions[5].id,  # Red
                 'value_suggested', self.labels[3].id, False, 'suggestion'),
                (self.user_inputs[1].id, self.questions[5].id,  # Yellow
                 'value_suggested', self.labels[5].id, False, 'suggestion'),
                (self.user_inputs[1].id, self.questions[6].id,  # Table Red
                 'value_suggested', self.labels[9].id, self.labels[6].id,
                 'suggestion'),
                (self.user_inputs[1].id, self.questions[6].id,  # Chair Red
                 'value_suggested', self.labels[9].id, self.labels[7].id,
                 'suggestion'),
                (self.user_inputs[1].id, self.questions[6].id,  # Door Green
                 'value_suggested', self.labels[10].id, self.labels[8].id,
                 'suggestion'),
                (self.user_inputs[1].id, self.questions[7].id,  # Wall Green
                 'value_suggested', self.labels[16].id, self.labels[12].id,
                 'suggestion'),
                (self.user_inputs[1].id, self.questions[7].id,  # Wall Yellow
                 'value_suggested', self.labels[17].id, self.labels[12].id,
                 'suggestion'),
                (self.user_inputs[1].id, self.questions[7].id,  # Desk Yellow
                 'value_suggested', self.labels[17].id, self.labels[13].id,
                 'suggestion'),
                (self.user_inputs[1].id, self.questions[7].id,  # Lamp Yellow
                 'value_suggested', self.labels[17].id, self.labels[14].id,
                 'suggestion'),

                # User_input 2
                (self.user_inputs[2].id, self.questions[0].id,
                 'value_free_text', 'Why not?', False, 'free_text'),
                (self.user_inputs[2].id, self.questions[1].id,
                 'value_text', 'The Who', False, 'text'),
                (self.user_inputs[2].id, self.questions[2].id,
                 'value_number', 42, False, 'number'),
                (self.user_inputs[2].id, self.questions[3].id,
                 'value_date', '2015-10-10 09:10:10', False, 'date'),
                (self.user_inputs[2].id, self.questions[4].id,  # Female
                 'value_suggested', self.labels[1].id, False, 'suggestion'),
                (self.user_inputs[2].id, self.questions[5].id,  # Yellow
                 'value_suggested', self.labels[5].id, False, 'suggestion'),
                (self.user_inputs[2].id, self.questions[6].id,  # Table Red
                 'value_suggested', self.labels[9].id, self.labels[6].id,
                 'suggestion'),
                (self.user_inputs[2].id, self.questions[6].id,  # Chair Red
                 'value_suggested', self.labels[9].id, self.labels[7].id,
                 'suggestion'),
                (self.user_inputs[2].id, self.questions[6].id,  # Door Red
                 'value_suggested', self.labels[9].id, self.labels[8].id,
                 'suggestion'),
                (self.user_inputs[2].id, self.questions[7].id,  # Wall Green
                 'value_suggested', self.labels[16].id, self.labels[12].id,
                 'suggestion'),
                (self.user_inputs[2].id, self.questions[7].id,  # Wall Yellow
                 'value_suggested', self.labels[17].id, self.labels[12].id,
                 'suggestion'),
                (self.user_inputs[2].id, self.questions[7].id,  # Desk Red
                 'value_suggested', self.labels[15].id, self.labels[13].id,
                 'suggestion'),
                (self.user_inputs[2].id, self.questions[7].id,  # Desk Yellow
                 'value_suggested', self.labels[17].id, self.labels[13].id,
                 'suggestion'),
                (self.user_inputs[2].id, self.questions[7].id,  # Lamp Red
                 'value_suggested', self.labels[15].id, self.labels[14].id,
                 'suggestion'),
                (self.user_inputs[2].id, self.questions[7].id,  # Lamp Green
                 'value_suggested', self.labels[16].id, self.labels[14].id,
                 'suggestion'),
                (self.user_inputs[2].id, self.questions[7].id,  # Lamp Yellow
                 'value_suggested', self.labels[17].id, self.labels[14].id,
                 'suggestion'),
            ]
        ]

        self.computation = self.ComputationObj.create({
            'name': 'Multiply by 2',
            'survey_id': self.survey.id,
            'python_code': 'result = q[%s] * 2\ntag = q[%s]'
                           % (self.questions[2].id, self.questions[1].id),
        })

    def test_get_questions_available(self):
        """
        Make sure question_ids fields is computed properly
        """
        self.assertEquals(
            self.computation.question_ids.mapped('id'),
            [x.id for x in self.questions],
        )

    def test_get_available_answers(self):
        """
        Make sure available answers fields for survey.question are properly
        computed
        """
        self.assertEqual(
            self.questions[4].available_answers_multiple,
            '[%s] Male\n[%s] Female\n[%s] Pineapple'
            % (self.labels[0].id, self.labels[1].id, self.labels[2].id)
        )
        self.assertEqual(
            self.questions[6].available_answers_matrix_type,
            '[%s] Red\n[%s] Green\n[%s] Yellow'
            % (self.labels[9].id, self.labels[10].id, self.labels[11].id)
        )
        self.assertEqual(
            self.questions[6].available_answers_matrix_row,
            '[%s] Table\n[%s] Chair\n[%s] Door'
            % (self.labels[6].id, self.labels[7].id, self.labels[8].id)
        )
        self.assertEqual(
            self.questions[6].multiple_answers_allowed,
            False
        )
        self.assertEqual(
            self.questions[7].multiple_answers_allowed,
            True
        )

    def test_compute_results(self):
        """
        Make results are correctly computed
        """
        self.computation.compute_all_inputs()
        results = self.ResultObj.search([
            ('survey_id', '=', self.survey.id)
        ])
        self.assertEqual(
            results[0].result,
            8.0,
        )
        self.assertEqual(
            results[0].tag,
            'Spice Girls',
        )
        self.assertEqual(
            results[1].result,
            24.0,
        )
        self.assertEqual(
            results[1].tag,
            'Queen',
        )
        self.assertEqual(
            results[2].result,
            84.0,
        )
        self.assertEqual(
            results[2].tag,
            'The Who',
        )
