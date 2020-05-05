from odoo.tests import common


class TestPartnerSurvey(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_partner_survey(self):
        test_partner = self.env["res.partner"].create({"name": "Company 1"})
        self.assertIs(type(test_partner.action_view_surveys()), dict)
        self.assertTrue(test_partner.surveys_invisible)
        self.assertTrue(test_partner.surveys_company_invisible)
