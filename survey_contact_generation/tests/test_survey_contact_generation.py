# Copyright 2023 Tecnativa - David Vidal
# Copyright 2023 Tecnativa - Stefan Ungureanu
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import HttpCase, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class SurveyContactGenerationCase(SurveyCase, HttpCase):
    def setUp(self):
        """We run the tour in the setup so we can share the tests case with other
        modules"""
        super().setUp()

        def _create_reference(obj):
            return f"{obj._name},{obj.id}"

        self.vendor_category = self.env["res.partner.category"].create(
            {
                "name": "Vendor",
            }
        )
        self.prospect_category = self.env["res.partner.category"].create(
            {
                "name": "Prospects",
            }
        )
        self.employee_category = self.env["res.partner.category"].create(
            {
                "name": "Employees",
            }
        )
        self.survey = self.env["survey.survey"].create(
            {
                "title": "Contact Creation Survey",
                "access_mode": "public",
                "users_can_go_back": True,
                "generate_contact": True,
                "create_parent_contact": True,
                "question_and_page_ids": [
                    Command.create(
                        {
                            "sequence": 0,
                            "title": "Company",
                            "question_type": "char_box",
                            "constr_mandatory": True,
                            "res_partner_field": self.env.ref(
                                "base.field_res_partner__company_name"
                            ).id,
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 1,
                            "title": "Name",
                            "question_type": "char_box",
                            "constr_mandatory": True,
                            "res_partner_field": self.env.ref(
                                "base.field_res_partner__name"
                            ).id,
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 2,
                            "title": "Email",
                            "question_type": "char_box",
                            "res_partner_field": self.env.ref(
                                "base.field_res_partner__email"
                            ).id,
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 3,
                            "title": "Notes",
                            "question_type": "text_box",
                            "res_partner_field": self.env.ref(
                                "base.field_res_partner__comment"
                            ).id,
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 4,
                            "title": "Color",
                            "question_type": "numerical_box",
                            "res_partner_field": self.env.ref(
                                "base.field_res_partner__color"
                            ).id,
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 6,
                            "title": "Country",
                            "question_type": "simple_choice",
                            "res_partner_field": self.env.ref(
                                "base.field_res_partner__country_id"
                            ).id,
                            "suggested_answer_ids": [
                                Command.create(
                                    {
                                        "sequence": 1,
                                        "value": "Spain",
                                        "res_partner_field_resource_ref": (
                                            _create_reference(self.env.ref("base.es"))
                                        ),
                                    }
                                ),
                                Command.create(
                                    {
                                        "sequence": 2,
                                        "value": "Romania",
                                        "res_partner_field_resource_ref": (
                                            _create_reference(self.env.ref("base.ro"))
                                        ),
                                    }
                                ),
                            ],
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 7,
                            "title": "Tags",
                            "question_type": "multiple_choice",
                            "res_partner_field": self.env.ref(
                                "base.field_res_partner__category_id"
                            ).id,
                            "suggested_answer_ids": [
                                Command.create(
                                    {
                                        "sequence": 1,
                                        "value": "Vendor",
                                        "res_partner_field_resource_ref": (
                                            _create_reference(self.vendor_category)
                                        ),
                                    }
                                ),
                                Command.create(
                                    {
                                        "sequence": 2,
                                        "value": "Prospects",
                                        "res_partner_field_resource_ref": (
                                            _create_reference(self.prospect_category)
                                        ),
                                    }
                                ),
                                Command.create(
                                    {
                                        "sequence": 3,
                                        "value": "Employees",
                                        "res_partner_field_resource_ref": (
                                            _create_reference(self.vendor_category)
                                        ),
                                    }
                                ),
                            ],
                        }
                    ),
                ],
            }
        )
        initial_user_inputs = self.survey.user_input_ids
        # Run the survey as a portal user and get the generated quotation
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_contact_generation",
        )
        self.user_input = self.survey.user_input_ids - initial_user_inputs


@tagged("-at_install", "post_install")
class SurveyContactGenerationTests(SurveyContactGenerationCase):
    def test_contact_generation(self):
        partner = self.env["res.partner"].search(
            [("email", "=", "survey_contact_generation@test.com")]
        )
        self.assertEqual(partner, self.user_input.partner_id)
        self.assertEqual(partner.parent_id.name, "My Company Name")
        self.assertEqual(partner.generating_survey_user_input_id, self.user_input)
