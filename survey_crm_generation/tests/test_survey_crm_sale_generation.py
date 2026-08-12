# Copyright 2023 Tecnativa - David Vidal
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from markupsafe import Markup

from odoo import Command
from odoo.tests import HttpCase, new_test_user, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class SurveyCrmGenerationCase(SurveyCase, HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()

        def _search_or_create(model, search, vals):
            Model = self.env[model]
            obj = Model.search(search)
            if obj:
                return obj
            return Model.create(vals)

        self.tag_survey_leads = _search_or_create(
            "crm.tag", [("name", "=", "Survey Leads")], {"name": "Survey Leads"}
        )
        self.tag_oca_partnership = _search_or_create(
            "crm.tag", [("name", "=", "OCA Partnership")], {"name": "OCA Partnership"}
        )
        self.oca_leads = _search_or_create(
            "crm.team", [("name", "=", "OCA Partnership")], {"name": "OCA Partnership"}
        )
        self.survey = self.env["survey.survey"].create(
            {
                "title": "Become OCA Partner",
                "description": "Be part of the Odoo Community!",
                "access_mode": "public",
                "generate_leads": True,
                "crm_team_id": self.oca_leads.id,
                "crm_tag_ids": [
                    Command.link(self.tag_oca_partnership.id),
                    Command.link(self.tag_survey_leads.id),
                ],
                "users_can_go_back": True,
                "question_and_page_ids": [
                    Command.create(
                        {
                            "sequence": 0,
                            "title": "E-mail address",
                            "question_type": "text_box",
                            "show_in_lead_description": True,
                            "constr_mandatory": True,
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 1,
                            "title": "Your company name?",
                            "question_type": "text_box",
                            "show_in_lead_description": True,
                            "constr_mandatory": True,
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 2,
                            "title": "And your name?",
                            "question_type": "text_box",
                            "show_in_lead_description": True,
                            "constr_mandatory": True,
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 6,
                            "title": "Referenced by",
                            "question_type": "simple_choice",
                            "comments_allowed": True,
                            "comment_count_as_answer": True,
                            "comments_message": "Other:",
                            "crm_lead_field": self.env.ref(
                                "crm.field_crm_lead__referred"
                            ).id,
                            "constr_mandatory": True,
                            "suggested_answer_ids": [
                                Command.create(
                                    {
                                        "sequence": 1,
                                        "value": "TV",
                                    }
                                ),
                                Command.create(
                                    {
                                        "sequence": 2,
                                        "value": "Internet",
                                    }
                                ),
                            ],
                        }
                    ),
                ],
            }
        )
        self.user = new_test_user(
            self.env, login="test-user", groups="base.group_portal"
        )

    def test_lead_generation(self):
        initial_user_inputs = self.survey.user_input_ids
        # Run the survey as a portal user and get the generated quotation
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_crm_generation",
            login="test-user",
        )
        self.user_input = self.survey.user_input_ids - initial_user_inputs
        self.generated_lead = self.user_input.opportunity_id
        self.assertFalse(self.generated_lead.stage_id.is_won)
        self.assertEqual(self.generated_lead.team_id, self.oca_leads)
        self.assertEqual(
            self.generated_lead.tag_ids,
            (self.tag_oca_partnership + self.tag_survey_leads),
        )
        expected_lead_description = Markup(
            "<li><em>E-mail address</em>: <b>test@test.com</b></li>"
            "<li><em>Your company name?</em>: <b>Tecnativa</b></li>"
            "<li><em>And your name?</em>: <b>Tecnativa</b></li>"
        )
        self.assertEqual(
            self.generated_lead.description,
            expected_lead_description,
        )
        self.assertEqual("Mr. Odoo", self.generated_lead.referred)
