# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo_test_helper import FakeModelLoader

from odoo.tests import tagged

from .test_survey_partner_representative import SurveyRepresentativeCase


@tagged("-at_install", "post_install")
class SurveyRepresentativeMixinCase(SurveyRepresentativeCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import ResPartner

        cls.loader.update_registry((ResPartner,))

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    def test_create_partner_representative_mixin(self):
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
        partner = self.env["res.partner"].create(
            {
                "name": "Test generated partner representative",
                "survey_user_input_id": self.user_input.id,
            }
        )
        self.assertEqual(
            partner.survey_representative_partner_id,
            self.portal_partner,
            "The representative partner should the one filling the survey",
        )
