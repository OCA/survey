# -*- coding: utf-8 -*-
# © initOS GmbH 2017
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re
from urlparse import urljoin
from odoo import fields

from odoo.addons.simple_poll.tests.common import TestPollQuestionCommon
from odoo.exceptions import UserError
from odoo.tests.common import HttpCase
import urllib2
from StringIO import StringIO


class TestSimplePollFlow(TestPollQuestionCommon):

    def test_poll_group(self):
        group_vals = {'name': 'test_poll_group',
                      'res_partner_ids': [(6, 0, [self.partner_id])]}
        self.poll_group = self.PollGroup.create(group_vals)
        self.assertEqual(True, bool(self.poll_group.name),
                         'Test Group has no name')
        self.assertEqual(1, len(self.poll_group.res_partner_ids),
                         'Test Group has no partner')
        self.assertEqual(True, bool(
            self.poll_group.res_partner_ids.email),
            'Test Group partner has no email')

    def test_public_url(self):
        def validate_url(url):
            """ Reference:
            https://github.com/django/django/
            blob/master/django/core/validators.py """
            url_regex = re.compile(
                r'^https?://'  # http:// or https://
                # domain...
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'
                r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
                r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return True if url_regex.match(url) else False

        base_url = self.IrConfigParam.get_param('web.base.url')
        url = "questions/%s?uuid=%s" % \
              (self.simple_text_question.id, self.simple_text_question.uuid)
        full_url = urljoin(base_url, url)
        self.assertTrue(validate_url(self.simple_text_question.public_url))
        self.assertEqual(full_url, self.simple_text_question.public_url)

    def test_send_by_email(self):
        action = self.choose_date_time_question.action_poll_send()
        try:
            template_id = self.IrModelData.get_object_reference(
                'simple_poll', 'email_template_edi_poll')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = self.IrModelData.get_object_reference(
                'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        ctx = dict()
        ctx.update({
            'default_model': 'poll.question',
            'default_res_id': self.choose_date_time_question.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
        })
        self.assertDictEqual(action, {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        })

    def test_poll_fields(self):
        self.assertEqual(True, bool(self.simple_text_question.title),
                         'Test Poll has no title')
        self.assertEqual(True, bool(self.simple_text_question.type),
                         'Test Group has no partner')
        self.assertEqual(True, bool(self.simple_text_question.end_date),
                         'Test Group partner has no email')

    def test_poll_mail_scheduler_run(self):
        self.assertEqual(True, self.poll_mail_scheduler.run())

    def test_poll_mail_scheduler_run_autocommit(self):
        self.assertEqual(True, self.poll_mail_scheduler.run(autocommit=True))

    def test_get_participant_emails(self):
        self.assertEqual(
            self.poll_group.res_partner_ids[0].email,
            self.simple_text_question.get_participant_emails()
        )

    def test_get_participants(self):
        self.assertEqual(
            set(self.poll_group.res_partner_ids[0]),
            self.simple_text_question.get_participants()
        )

    def test_get_participants_no_answer(self):
        self.assertEqual(
            set(self.poll_group.res_partner_ids[0]),
            self.simple_text_question.get_participants_no_answer()
        )

    def test_poll_group_create_error(self):
        res_partner = self.ResPartner.create({
            'name': 'Test Partner NO EMAIL',
        })
        group_vals = {'name': 'Poll Group Test',
                      'res_partner_ids': [(6, 0, [res_partner.id])]}
        with self.assertRaises(UserError):
            self.PollGroup.create(group_vals)

    def test_poll_group_write_error(self):
        group_vals = {'name': 'Poll Group Test'}
        with self.assertRaises(UserError):
            group = self.PollGroup.create(group_vals)
            res_partner = self.ResPartner.create({
                'name': 'Test Partner NO EMAIL',
            })
            group.write({
                'res_partner_ids': [(6, 0, [res_partner.id])]})

    def test_poll_group_write(self):
        group_vals = {'name': 'Poll Group Test'}
        group = self.PollGroup.create(group_vals)
        res_partner = self.ResPartner.create({
            'name': 'Test Partner with email',
            'email': 'test@myexample.com'
        })
        group.write({
            'res_partner_ids': [(6, 0, [res_partner.id])]})

        self.assertEqual(res_partner.id, group.res_partner_ids[0].id,
                         'Test Group has added a partner')

    def test_save_answer_yes_no_maybe(self):
        pos = {
            'res_partner_id': self.poll_group.res_partner_ids[0].id,
            str(self.simple_text_question.option_ids[0].id): '1',
        }

        self.QuestionAnswer.save_answer(self.simple_text_question, pos)
        answer = \
            self.QuestionAnswer.search([
                ('question_id', '=', self.simple_text_question.id),
                ('res_partner_id', '=', pos['res_partner_id']),
                (
                    'option_id',
                    '=',
                    self.simple_text_question.option_ids[0].id
                )
            ])
        if not answer:
            answer = None
        self.assertIsNotNone(answer)
        self.assertEqual('1', answer.answer)

        pos[str(self.simple_text_question.option_ids[0].id)] = '3'
        self.QuestionAnswer.save_answer(self.simple_text_question, pos)

        answer = \
            self.QuestionAnswer.search([
                ('question_id', '=', self.simple_text_question.id),
                ('res_partner_id', '=', pos['res_partner_id']),
                (
                    'option_id',
                    '=',
                    self.simple_text_question.option_ids[0].id
                )
            ])

        if not answer:
            answer = None
        self.assertIsNotNone(answer)
        self.assertEqual('3', answer.answer)

    def test_save_answer_yes_no(self):
        firs_option_id = self.choose_date_question.option_ids[0].id
        second_option_id = self.choose_date_question.option_ids[1].id

        pos = {
            'res_partner_id': self.poll_group.res_partner_ids[0].id,
            str(firs_option_id): ''
        }

        self.QuestionAnswer.save_answer(self.choose_date_question, pos)
        answer_firs_option = \
            self.QuestionAnswer.search([
                ('question_id', '=', self.choose_date_question.id),
                ('res_partner_id', '=', pos['res_partner_id']),
                (
                    'option_id',
                    '=',
                    firs_option_id,
                )
            ])
        answer_second_option = \
            self.QuestionAnswer.search([
                ('question_id', '=', self.choose_date_question.id),
                ('res_partner_id', '=', pos['res_partner_id']),
                (
                    'option_id',
                    '=',
                    second_option_id,
                )
            ])
        if not answer_firs_option:
            answer_firs_option = None
        if not answer_second_option:
            answer_second_option = None

        self.assertIsNotNone(answer_firs_option)
        self.assertEqual('1', answer_firs_option.answer)

        self.assertIsNotNone(answer_second_option)
        self.assertEqual('2', answer_second_option.answer)


class UICase(HttpCase):
    def setUp(self):
        super(UICase, self).setUp()
        self.PollQuestion = self.env['poll.question']
        self.choose_date_question = self.PollQuestion.create({
            'title': 'Choose Date Question',
            'type': 'date',
            'end_date': fields.Datetime.now(),
            'yes_no_maybe': False,
            'option_ids': [
                (0, 0, {'name_date': fields.Date.today()}),
                (0, 0, {'name_date': fields.Date.from_string('2018-08-30')}),
            ],
        })

    def mock_response(self, req, uuid):
        url = self.choose_date_question.public_url
        poll_uuid = self.choose_date_question.uuid
        if req.geturl() == url and poll_uuid == uuid:
            resp = \
                urllib2.addinfourl(
                    StringIO("mock file"),
                    "mock message",
                    req.geturl()
                )
            resp.code = 200
            resp.msg = "OK"
            return resp
        if req.geturl() == url and poll_uuid != uuid:
            resp = \
                urllib2.addinfourl(
                    StringIO("mock file"),
                    "mock message",
                    req.geturl()
                )
            resp.code = 404
            resp.msg = "Error"
            return resp

    def test_uuid_ok(self):
        """Test uuid ok."""
        url = self.choose_date_question.public_url
        uuid = self.choose_date_question.uuid
        result = self.url_open(url, uuid, 30)
        result = self.mock_response(result, uuid)
        self.assertEqual(200, result.code)

    def test_uuid_error(self):
        """Test uuid error."""
        url = self.choose_date_question.public_url
        uuid = self.choose_date_question.uuid + '12'
        result = self.url_open(url, uuid, 30)
        result = self.mock_response(result, uuid)
        self.assertEqual(404, result.code)
