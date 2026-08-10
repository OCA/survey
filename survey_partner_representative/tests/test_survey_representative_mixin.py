# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.orm.model_classes import add_to_registry
from odoo.tests import tagged

from .test_survey_partner_representative import SurveyRepresentativeCase


@tagged("-at_install", "post_install")
class SurveyRepresentativeMixinCase(SurveyRepresentativeCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from .models import ResPartner

        add_to_registry(cls.registry, ResPartner)
        cls.registry._setup_models__(cls.env.cr, ["test.model"])
        cls.registry.init_models(cls.env.cr, ["test.model"], {"models_to_check": True})
        cls.addClassCleanup(cls.registry.__delitem__, "test.model")

    def test_create_partner_representative_mixin(self):
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
        partner = self.env["test.model"].create(
            {
                "survey_user_input_id": self.user_input.id,
            }
        )
        self.assertEqual(
            partner.survey_representative_partner_id.id,
            self.user.partner_id.id,
            "The representative partner should the one filling the survey",
        )
