# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestSurvey(TransactionCase):
    def setUp(self):
        super(TestSurvey, self).setUp()
        User = self.env['res.users'].with_context({'no_reset_password': True})
        (group_survey_user, group_employee) = (
            self.ref('survey.group_survey_user'),
            self.ref('base.group_user'),
        )
        self.survey_manager = User.create(
            {
                'name': 'Gustave Doré',
                'login': 'Gustav',
                'email': 'gustav.dore@example.com',
                'groups_id': [
                    (
                        6,
                        0,
                        [
                            self.ref('survey.group_survey_manager'),
                            group_survey_user,
                            group_employee,
                        ],
                    )
                ],
            }
        )
        self.survey1 = (
            self.env['survey.survey']
            .sudo(self.survey_manager)
            .create({'title': "S0", 'page_ids': [(0, 0, {'title': "P0"})]})
        )
        self.page1 = self.survey1.page_ids[0]
        self.user_input1 = (
            self.env['survey.user_input']
            .sudo(self.survey_manager)
            .create(
                {
                    'survey_id': self.survey1.id,
                    'partner_id': self.survey_manager.partner_id.id,
                }
            )
        )
        self.question1 = (
            self.env['survey.question']
            .sudo(self.survey_manager)
            .create(
                {
                    'page_id': self.page1.id,
                    'question': 'Q0',
                    'type': 'star_rate',
                    'validation_required': True,
                }
            )
        )
        self.answer_tag1 = '%s_%s_%s' % (
            self.survey1.id,
            self.page1.id,
            self.question1.id,
        )

    def test_01_question_star_rate_with_error_values(self):
        error_results = [
            ('aaa', 'This is not a number'),
            ('-1', 'Answer is not in the right range'),
            ('6', 'Answer is not in the right range'),
        ]
        msg = "Validation function for type numerical_box is unable to " \
              "notify if answer is violating the validation rules"
        for i in range(len(error_results)):
            self.assertEqual(
                self.question1.validate_question(
                    {self.answer_tag1: error_results[i][0]}, self.answer_tag1
                ),
                {self.answer_tag1: error_results[i][1]},
                msg=msg,
            )

    def test_02_question_star_rate_with_valid_values(self):
        for i in ('0', '3', '5'):
            self.assertTrue(
                self.env['survey.user_input_line'].save_line_star_rate(
                    user_input_id=self.user_input1.id,
                    question=self.question1,
                    post={self.answer_tag1: i},
                    answer_tag=self.answer_tag1,
                )
            )

    def test_03_question_star_rate_with_constr_mandatory(self):
        self.question1.constr_mandatory = True
        with self.assertRaises(ValidationError):
            self.env['survey.user_input_line'].save_line_star_rate(
                user_input_id=self.user_input1.id,
                question=self.question1,
                post={self.answer_tag1: '0'},
                answer_tag=self.answer_tag1,
            )
