# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import datetime

from freezegun import freeze_time

from odoo.exceptions import UserError
from odoo.tests.common import Form, TransactionCase

from ...resource_booking.tests.common import create_test_data


@freeze_time("2021-02-26 09:00:00", tick=True)
class SurveyInvitationCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_test_data(cls)
        survey_form = Form(cls.env["survey.survey"])
        survey_form.title = "survey 1"
        survey_form.session_state = "in_progress"
        with survey_form.question_and_page_ids.new() as question_form:
            question_form.title = "are you a robot?"
            question_form.question_type = "text_box"
        cls.survey = survey_form.save()
        cls.rbt.survey_id = cls.survey

    def test_new_booking_survey_invitation(self):
        """New booking gets invited to survey."""
        # Clear mail queue to avoid pollution
        self.env["mail.mail"].search([]).unlink()
        # Make sure RB gets surveyed as expected
        booking_f = Form(self.env["resource.booking"])
        booking_f.type_id = self.rbt
        booking_f.partner_id = self.partner
        booking_f.start = datetime(2021, 3, 1, 8)
        booking = booking_f.save()
        self.assertEqual(booking.state, "scheduled")
        self.assertFalse(booking.survey_user_input_id)
        self.assertEqual(len(self.env["mail.mail"].search([])), 1)
        # Nope
        with self.assertRaises(UserError):
            booking.action_invite_survey()
        self.assertEqual(booking.state, "scheduled")
        self.assertFalse(booking.survey_user_input_id)
        self.assertEqual(len(self.env["mail.mail"].search([])), 1)
        # After confirming, also nope: partner without email
        booking.action_confirm()
        with self.assertRaises(UserError):
            booking.action_invite_survey()
        # Bad mail? Nope
        self.partner.email = "I'm tricking you"
        with self.assertRaises(UserError):
            booking.action_invite_survey()
        # After setting good mail, yep
        self.partner.email = "donkey@banana.kong"
        booking.action_invite_survey()
        self.assertEqual(booking.state, "confirmed")
        self.assertTrue(booking.survey_user_input_id)
        self.assertTrue(len(self.env["mail.mail"].search([])), 2)
