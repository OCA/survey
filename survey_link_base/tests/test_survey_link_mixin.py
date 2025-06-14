# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo_test_helper import FakeModelLoader

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

TEST_MODEL_NAME = "test.survey.mixin"


@tagged("post_install", "-at_install")
class TestSurveyLinkMixin(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        loader = FakeModelLoader(cls.env, cls.__module__)
        loader.backup_registry()
        from .models import TestSurveyMixinModel

        loader.update_registry((TestSurveyMixinModel,))
        partner = cls.env["res.partner"].create(
            {"name": "TestPartner", "email": "test@test.com"}
        )
        cls.test_record = cls.env[TEST_MODEL_NAME].create(
            {
                "name": "Test Record",
                "partner_id": partner.id,
            }
        )
        cls.survey = cls.env["survey.survey"].create({"title": "Survey Test"})

    def test_action_survey_link_wizard(self):
        action = self.test_record.action_survey_link_wizard()
        self.assertTrue(action)
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "survey.link.wizard")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["context"]["default_res_id"], self.test_record.id)
        self.assertEqual(action["context"]["default_res_model"], self.test_record._name)
        self.assertEqual(
            action["context"]["default_partner_id"], self.test_record.partner_id.id
        )

    def test_action_view_survey_answer(self):
        action = self.test_record.action_view_survey_answer()
        self.assertTrue(action)
        self.assertEqual(
            action["domain"],
            [
                ("res_id", "=", self.test_record.id),
                ("res_model", "=", self.test_record._name),
                ("partner_id", "=", self.test_record.partner_id.id),
            ],
        )
        self.assertEqual(action["context"]["default_res_id"], self.test_record.id)
        self.assertEqual(action["context"]["default_res_model"], self.test_record._name)
        self.assertEqual(
            action["context"]["default_partner_id"], self.test_record.partner_id.id
        )
        self.assertFalse(action["context"]["default_survey_id"])

    def test_get_default_survey(self):
        self.assertFalse(self.test_record.get_default_survey())
        self.assertTrue(
            self.test_record.with_context(
                **{"default_survey_id": self.survey.id}
            ).get_default_survey()
        )

    def test_get_share_link(self):
        share_link = self.test_record.get_share_link()
        self.assertFalse(share_link)
        share_link = self.test_record.with_context(
            **{"default_survey_id": self.survey.id}
        ).get_share_link()
        self.assertTrue(share_link)
        self.assertIn("survey", share_link)
        self.assertIn(self.survey.access_token, share_link)

    def test_compute_survey_answer_count(self):
        self.assertEqual(self.test_record.survey_answer_count, 0)
        self.survey._create_answer(
            email=self.test_record.partner_id.email,
            partner=self.test_record.partner_id,
            res_id=self.test_record.id,
            res_model=self.test_record._name,
        )
        self.test_record._compute_survey_answer_count()
        self.assertEqual(self.test_record.survey_answer_count, 1)
