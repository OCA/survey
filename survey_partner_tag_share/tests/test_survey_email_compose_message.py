# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp.tests import TransactionCase


class TestSurveyEmailComposeMessage(TransactionCase):

    def setUp(self):

        super(TestSurveyEmailComposeMessage, self).setUp()

        self.PartnerObj = self.env['res.partner']
        self.PartnerCategoryObj = self.env['res.partner.category']
        self.SurveyObj = self.env['survey.survey']
        self.SurveyPageObj = self.env['survey.page']
        self.SurveyQuestionObj = self.env['survey.question']
        self.SurveyLabelObj = self.env['survey.label']
        self.WizardObj = self.env['survey.mail.compose.message']

        self.partners = [
            self.PartnerObj.create({
                'name': record[0],
                'email': record[1],
            }) for record in [
                ('test0', 'test0@test_example.com'),
                ('test1', 'test1@test_example.com'),
                ('test2', 'test2@test_example.com'),
                ('test3', 'test3@test_example.com'),
                ('test4', 'test4@test_example.com'),
                ('test5', 'test5@test_example.com'),
                ('test6', 'test6@test_example.com'),
            ]
        ]

        self.tag = self.PartnerCategoryObj.create({
            'name': 'Test tag',
            'partner_ids': [(6, 0, [self.partners[i].id for i in range(4)])]
        })

        self.survey = self.SurveyObj.create({
            'title': 'Survey Test',
        })

        self.wizard = self.WizardObj.create({
            'survey_id': self.survey.id,
            'public': 'email_private',
            'tags': [(6, 0, [self.tag.id])],
            'partners_manual': [(6, 0,
                                 [self.partners[i].id for i in range(4, 6)])]
        })

    def test_get_recipients(self):
        """
        Make sure partner_ids field is computed properly
        """
        self.assertEquals(
            [p.id for p in self.wizard.partner_ids],
            [self.partners[i].id for i in range(6)],
        )
