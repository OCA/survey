# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestSurveyLinkBase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.res_id = 111
        cls.res_model = "test.model"
        cls.survey = cls.env["survey.survey"].create({"title": "Survey Test"})
        cls.partner_id = cls.env["res.partner"].create(
            {"name": "Partner Test", "email": "partner_test@test.com"}
        )

        cls.SurveyLinkWizard = cls.env["survey.link.wizard"]

    def test_survey_link_wizard(self):
        wizard = self.SurveyLinkWizard.create(
            {
                "survey_id": self.survey.id,
                "partner_id": self.partner_id.id,
                "res_id": self.res_id,
                "res_model": self.res_model,
            }
        )
        self.assertTrue(wizard)
        self.assertEqual(wizard.survey_id.id, self.survey.id)
        self.assertEqual(wizard.partner_id.id, self.partner_id.id)
        self.assertIn("survey", wizard.share_link)
        self.assertIn(self.survey.access_token, wizard.share_link)
        user_input = self.env["survey.user_input"].search(
            [
                ("res_id", "=", self.res_id),
                ("res_model", "=", self.res_model),
                ("partner_id", "=", self.partner_id.id),
            ]
        )
        self.assertTrue(user_input)
        self.assertEqual(len(user_input), 1)
        self.assertEqual(user_input.survey_id.id, self.survey.id)
        self.assertEqual(user_input.partner_id.id, self.partner_id.id)
        self.assertEqual(user_input.res_id, self.res_id)
        self.assertEqual(user_input.res_model, self.res_model)
        self.assertIn(user_input.access_token, wizard.share_link)

        action = wizard.action_start_survey()
        self.assertTrue(action)
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertIn(action["url"], wizard.share_link)
        self.assertEqual(action["target"], "new")
