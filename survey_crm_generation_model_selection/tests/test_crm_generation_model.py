# Copyright 2026 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from markupsafe import Markup

from odoo import Command
from odoo.tests import HttpCase, new_test_user, tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("-at_install", "post_install")
class SurveyCrmGenerationCase(BaseCommon, HttpCase):
    @classmethod
    def setUpClass(cls):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUpClass()
        cls.user = new_test_user(cls.env, login="test-user", groups="base.group_portal")
        cls.reference = cls.env["res.partner"].create({"name": "Reference Partner"})
        cls.tag_lead = cls.env["crm.tag"].create({"name": "Survey"})
        cls.tag_lead_partnership = cls.env["crm.tag"].create({"name": "Partnership"})
        cls.team_partnership = cls.env["crm.team"].create({"name": "Partnership"})
        cls.survey = cls.env["survey.survey"].create(
            {
                "title": "Become Partner",
                "survey_type": "custom",
                "questions_layout": "one_page",
                "access_mode": "public",
                "access_token": "b137640d-14d4-4748-9ef6-344caaaaaafff",
                "crm_team_id": cls.team_partnership.id,
                "crm_tag_ids": [
                    Command.set([cls.tag_lead.id, cls.tag_lead_partnership.id])
                ],
                "generate_leads": True,
            }
        )
        cls.question = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Name",
                "question_type": "char_box",
                "show_in_lead_description": True,
            }
        )
        cls.question = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Email",
                "question_type": "char_box",
                "show_in_lead_description": True,
            }
        )
        cls.question = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Country",
                "question_type": "model",
                "question_model_id": cls.env["ir.model"]._get_id("res.country"),
                "crm_lead_field": cls.env.ref("crm.field_crm_lead__country_id").id,
            }
        )

    def test_lead_generation(self):
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_crm_question_model",
            login="test-user",
        )
        self.generated_lead = self.survey.user_input_ids.opportunity_id
        self.assertFalse(self.generated_lead.stage_id.is_won)
        self.assertEqual(self.generated_lead.team_id, self.team_partnership)
        self.assertEqual(
            self.generated_lead.tag_ids,
            (self.tag_lead + self.tag_lead_partnership),
        )
        expected_lead_description = Markup(
            "<li><em>Name</em>: <b>Tecnativa</b></li>"
            "<li><em>Email</em>: <b>test@test.com</b></li>"
        )
        self.assertEqual(
            self.generated_lead.description,
            expected_lead_description,
        )
        self.assertEqual(self.generated_lead.country_id.name, "Algeria")
