# Copyright 2024 Tecnativa - David Vidal
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import HttpCase, new_test_user, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class SurveyRepresentativeCase(SurveyCase, HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()
        self.user = new_test_user(
            self.env, login="test-user", name="test user", email="testuser@test.com"
        )
        self.representative_group = self.env.ref(
            "survey_partner_representative.partner_representative"
        )
        survey_vals = {
            "title": "Meal preferences",
            "access_mode": "public",
            "users_can_go_back": True,
            "question_and_page_ids": [
                Command.create(
                    {
                        "sequence": 0,
                        "title": "Name",
                        "question_type": "char_box",
                        "constr_mandatory": True,
                    }
                ),
                Command.create(
                    {
                        "sequence": 1,
                        "title": "Email",
                        "question_type": "char_box",
                    }
                ),
                Command.create(
                    {
                        "sequence": 4,
                        "title": "What would you like for dinner?",
                        "question_type": "simple_choice",
                        "suggested_answer_ids": [
                            Command.create(
                                {
                                    "sequence": 1,
                                    "value": "Meat",
                                }
                            ),
                            Command.create(
                                {
                                    "sequence": 2,
                                    "value": "Fish",
                                }
                            ),
                            Command.create(
                                {
                                    "sequence": 3,
                                    "value": "Vegan",
                                }
                            ),
                        ],
                    }
                ),
            ],
        }
        self.survey = self.env["survey.survey"].create(survey_vals)

    def _do_survey(self):
        """Run the survey common method"""
        initial_user_inputs = self.survey.user_input_ids
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_representative",
            login="test-user",
        )
        self.user_input = self.survey.user_input_ids - initial_user_inputs


@tagged("-at_install", "post_install")
class SurveyRepresentativeTests(SurveyRepresentativeCase):
    def test_not_survey_representative_not_allowed_partner(self):
        """A survey that can't be filled by representatives and a user who doesn't
        have the permissions"""
        self._do_survey()
        self.assertEqual(
            self.user_input.partner_id.id,
            self.user.partner_id.id,
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
            self.user_input.partner_id.id,
            self.user.partner_id.id,
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
        self.representative_group.all_user_ids |= self.user
        self._do_survey()
        self.assertEqual(
            self.user_input.partner_id.id,
            self.user.partner_id.id,
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
        self.representative_group.all_user_ids |= self.user
        self.survey.allow_partner_representing = True
        self._do_survey()
        self.assertEqual(
            self.user_input.partner_id,
            self.env["res.partner"],
            "he partner should be empty",
        )
        self.assertEqual(
            self.user_input.representative_partner_id.id,
            self.user.partner_id.id,
            "The representative partner should the one filling the survey",
        )
