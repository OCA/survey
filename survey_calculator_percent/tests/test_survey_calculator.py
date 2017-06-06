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

from openerp.addons.survey_calculator.tests.test_survey_calculator import \
    TestSurveyCalculator


class TestSurveyCalculatorPercent(TestSurveyCalculator):

    def setUp(self):

        super(TestSurveyCalculatorPercent, self).setUp()

        self.question_percent = self.SurveyQuestionObj.create({
            'page_id': self.page.id,
            'question': 'What is the men/women ratio?',
            'type': 'percent_split',
        })
        self.questions.append(self.question_percent)

        self.label_men = self.SurveyLabelObj.create({
            'question_id': self.question_percent.id,
            'value': 'Men',
        })
        self.label_women = self.SurveyLabelObj.create({
            'question_id': self.question_percent.id,
            'value': 'Women',
        })
        self.labels += [self.label_men, self.label_women]

        self.input_0_men = self.SurveyUserInputLineObj.create({
            'user_input_id': self.user_inputs[0].id,
            'question_id': self.question_percent.id,
            'value_suggested_row': self.label_men.id,
            'value_number': 50,
            'answer_type': 'number',
        })
        self.input_0_women = self.SurveyUserInputLineObj.create({
            'user_input_id': self.user_inputs[0].id,
            'question_id': self.question_percent.id,
            'value_suggested_row': self.label_women.id,
            'value_number': 50,
            'answer_type': 'number',
        })
        self.input_1_men = self.SurveyUserInputLineObj.create({
            'user_input_id': self.user_inputs[1].id,
            'question_id': self.question_percent.id,
            'value_suggested_row': self.label_men.id,
            'value_number': 40,
            'answer_type': 'number',
        })
        self.input_1_women = self.SurveyUserInputLineObj.create({
            'user_input_id': self.user_inputs[1].id,
            'question_id': self.question_percent.id,
            'value_suggested_row': self.label_women.id,
            'value_number': 60,
            'answer_type': 'number',
        })
        self.input_2_men = self.SurveyUserInputLineObj.create({
            'user_input_id': self.user_inputs[2].id,
            'question_id': self.question_percent.id,
            'value_suggested_row': self.label_men.id,
            'value_number': 48.3,
            'answer_type': 'number',
        })
        self.input_2_women = self.SurveyUserInputLineObj.create({
            'user_input_id': self.user_inputs[2].id,
            'question_id': self.question_percent.id,
            'value_suggested_row': self.label_women.id,
            'value_number': 51.7,
            'answer_type': 'number',
        })

    def test_get_available_answers_percent(self):
        """
        Make sure available answers fields for survey.question are properly
        computed
        """
        self.assertEqual(
            self.question_percent.available_answers_multiple,
            '[%s] Men\n[%s] Women' % (self.label_men.id, self.label_women.id)
        )
        self.assertEqual(
            self.question_percent.multiple_answers_allowed,
            False
        )

    def test_compute_results_percent(self):
        """
        Make results are correctly computed
        """
        self.result_percent = self.ResultObj.create({
            'user_input_id': self.user_inputs[0].id,
            'computation_id': self.computation.id,
        })
