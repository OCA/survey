# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import tagged

from odoo.addons.survey_sale_generation.tests.test_survey_sale_generation import (
    SurveySaleGenerationCase,
)


@tagged("-at_install", "post_install")
class SurveyCrmSaleGenerationTests(SurveySaleGenerationCase):
    def test_lead_generation(self):
        """This test is a follow up for SurveySaleGenerationTests. The generated sale
        is linked to a new opportunity/lead and the data defined in the survey should
        be passed to it. When we confirm the linked sale, the lead is set as won.
        """
        opportunity = self.user_input.opportunity_id
        self.assertFalse(opportunity.stage_id.is_won)
        self.assertEqual(opportunity.team_id, self.support_hiring_team)
        self.assertEqual(
            opportunity.tag_ids,
            (
                self.env.ref("survey_crm_sale_generation.tag_tech_support")
                + self.env.ref("survey_crm_generation.tag_survey_leads")
            ),
        )
        self.generated_sale.action_confirm()
        self.assertTrue(opportunity.stage_id.is_won)
