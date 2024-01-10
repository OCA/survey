# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import HttpCase, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class SurveyRepresentativeCase(SurveyCase, HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.portal_partner = self.env.ref("base.partner_demo_portal")
        self.portal_user = self.env.ref("base.demo_user0")
        self.representative_group = self.env.ref(
            "survey_partner_representative.partner_representative"
        )
        self.survey = self.env.ref(
            "survey_partner_representative.survey_representative_demo"
        )

    def _do_survey(self):
        """Run the survey common method"""
        initial_user_inputs = self.survey.user_input_ids
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_representative",
            login="portal",
        )
        self.user_input = self.survey.user_input_ids - initial_user_inputs


@tagged("-at_install", "post_install")
class SurveyRepresentativeTests(SurveyRepresentativeCase):
    def test_not_survey_representative_not_allowed_partner(self):
        """A survey that can't be filled by representatives and a user who doesn't
        have the permissions"""
        self._do_survey()
        self.assertEqual(
            self.user_input.partner_id,
            self.portal_partner,
            "The partner should be the one filling the survey",
        )
        self.assertEqual(
            self.user_input.representative_partner_id,
            self.env["res.partner"],
            "The representative partner should be empty",
        )

    def test_survey_allowed_representative_not_allowed_partner(self):
        """A survey that can be filled by representatives and a user who doesn't have
        the permissions"""
        self.survey.allow_partner_representing = True
        self._do_survey()
        self.assertEqual(
            self.user_input.partner_id,
            self.portal_partner,
            "The partner should be the one filling the survey",
        )
        self.assertEqual(
            self.user_input.representative_partner_id,
            self.env["res.partner"],
            "The representative partner should be empty",
        )

    def test_survey_not_representative_not_allowed_partner(self):
        """A survey that can't be filled by representatives and a user who has
        the permissions"""
        self.representative_group.users |= self.portal_user
        self._do_survey()
        self.assertEqual(
            self.user_input.partner_id,
            self.portal_partner,
            "The partner should be the one filling the survey",
        )
        self.assertEqual(
            self.user_input.representative_partner_id,
            self.env["res.partner"],
            "The representative partner should be empty",
        )

    def test_survey_allowd_representative_allowed_partner(self):
        """A survey that can't be filled by representatives and a user who has
        the permissions"""
        self.representative_group.users |= self.portal_user
        self.survey.allow_partner_representing = True
        self._do_survey()
        self.assertEqual(
            self.user_input.partner_id,
            self.env["res.partner"],
            "he partner should be empty",
        )
        self.assertEqual(
            self.user_input.representative_partner_id,
            self.portal_partner,
            "The representative partner should the one filling the survey",
        )
