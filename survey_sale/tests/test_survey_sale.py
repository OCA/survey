# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestSurveySale(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = cls.env["survey.survey"].create({"title": "Survey Test"})
        cls.partner_id = cls.env["res.partner"].create(
            {"name": "Test Partner", "email": "test@test.com"}
        )
        cls.company = cls.env.company
        cls.sale = cls.env["sale.order"].create(
            {
                "name": "Test Sale",
                "company_id": cls.company.id,
                "partner_id": cls.partner_id.id,
            }
        )

    def test_get_default_survey(self):
        self.company.survey_sale_id = False
        self.assertFalse(self.sale.get_default_survey())
        self.company.survey_sale_id = self.survey.id
        self.assertEqual(self.sale.get_default_survey(), self.survey.id)
