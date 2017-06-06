# -*- coding: utf-8 -*-
#
from openerp.tests import common


class TestPartnerSurvey(common.TransactionCase):

    def setUp(self):
        super(TestPartnerSurvey, self).setUp()
        self.data = self.env['ir.model.data']

        self.survey_id = self.data.xmlid_to_res_id(
            'survey.feedback_form')
        self.survey_obj = self.env['survey.survey']
        self.survey = self.survey_obj.browse(
            self.survey_id)

        self.partner_id = self.data.xmlid_to_res_id(
            'base.res_partner_1')
        self.partner_obj = self.env['res.partner']
        self.partner = self.partner_obj.browse(
            self.partner_id)

        self.fill_survey_obj = self.env['fill.survey']
        self.user_input_obj = self.env['survey.user_input']

    def test_01_wizard(self):
        ctx = dict(self.env.context)
        ctx.update({
            'active_id': self.partner_id,
            'active_model': 'res.partner'
        })
        values = self.fill_survey_obj.with_context(ctx).default_get([])
        values.update({'survey_id': self.survey_id})
        wizard = self.fill_survey_obj.create(values)
        self.assertEqual(
            self.partner_id,
            wizard.partner_id.id
        )
        res = wizard.open_survey()
        self.assertEqual(
            res.get('type'),
            'ir.actions.act_url'
        )
        self.assertEqual(
            res.get('target'),
            'self'
        )
        url = res.get('url')
        elements = url.split('/')
        token = elements[-1]
        user_input = self.user_input_obj.search([('token', '=', token)])
        user_input.ensure_one()
        self.assertEqual(
            user_input.partner_id.id,
            self.partner_id
        )
        self.assertEqual(
            user_input.survey_id.id,
            self.survey_id
        )
