# Copyright 2023 Tecnativa - David Vidal
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import tagged

from odoo.addons.survey_sale_generation.tests.test_survey_sale_generation import (
    SurveySaleGenerationCase,
)


@tagged("-at_install", "post_install")
class SurveyCrmSaleGenerationTests(SurveySaleGenerationCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        def _ref_or_create(model, ref, vals):
            record = cls.env.ref(ref, raise_if_not_found=False)
            return record or cls.env[model].create(vals)

        cls.tag_tech_support = _ref_or_create(
            model="crm.tag",
            ref="survey_crm_sale_generation.tag_tech_support",
            vals={"name": "Tech support"},
        )
        cls.tag_survey_leads = _ref_or_create(
            model="crm.tag",
            ref="survey_crm_generation.tag_survey_leads",
            vals={"name": "Survey Leads"},
        )
        cls.survey.write(
            {
                "generate_leads": True,
                "crm_tag_ids": [
                    Command.set([cls.tag_tech_support.id, cls.tag_survey_leads.id])
                ],
            }
        )

    def test_lead_generation(self):
        """This test is a follow up for SurveySaleGenerationTests. The generated sale
        is linked to a new opportunity/lead and the data defined in the survey should
        be passed to it. When we confirm the linked sale, the lead is set as won.
        """
        initial_user_inputs = self.survey.user_input_ids
        # Run the survey as a portal user and get the generated quotation
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_sale_generation",
            login="test-user",
        )
        self.user_input = self.survey.user_input_ids - initial_user_inputs
        opportunity = self.user_input.opportunity_id
        self.generated_sale = self.user_input.sale_order_id
        self.assertFalse(opportunity.stage_id.is_won)
        self.assertEqual(opportunity.team_id, self.support_hiring_team)
        self.assertEqual(
            opportunity.tag_ids, self.tag_tech_support + self.tag_survey_leads
        )
        self.generated_sale.action_confirm()
        self.assertTrue(opportunity.stage_id.is_won)
