# Copyright 2024 Tecnativa - David Vidal
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import HttpCase, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class SurveyNextSurveyUpdatePartnerCase(SurveyCase, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        def _create_reference(obj):
            return f"{obj._name},{obj.id}"

        ResPartnerCategory = cls.env["res.partner.category"]
        SurveySurvey = cls.env["survey.survey"]
        SurveyQuestion = cls.env["survey.question"]
        cls.vendor_category = ResPartnerCategory.create(
            {
                "name": "Vendor",
            }
        )
        cls.prospect_category = ResPartnerCategory.create(
            {
                "name": "Prospects",
            }
        )
        cls.employee_category = ResPartnerCategory.create(
            {
                "name": "Employees",
            }
        )
        survey_contact_q0 = SurveyQuestion.create(
            {
                "sequence": 1,
                "title": "Name",
                "question_type": "char_box",
                "constr_mandatory": True,
                "res_partner_field": cls.env.ref("base.field_res_partner__name").id,
            }
        )
        survey_contact_q_company_name = SurveyQuestion.create(
            {
                "sequence": 0,
                "title": "Company",
                "question_type": "char_box",
                "constr_mandatory": True,
                "res_partner_field": cls.env.ref(
                    "base.field_res_partner__company_name"
                ).id,
            }
        )
        questions_vals = (
            [
                Command.link(survey_contact_q_company_name.id),
                Command.link(survey_contact_q0.id),
                Command.create(
                    {
                        "sequence": 2,
                        "title": "Email",
                        "question_type": "char_box",
                        "res_partner_field": cls.env.ref(
                            "base.field_res_partner__email"
                        ).id,
                    }
                ),
                Command.create(
                    {
                        "sequence": 3,
                        "title": "Notes",
                        "question_type": "text_box",
                        "res_partner_field": cls.env.ref(
                            "base.field_res_partner__comment"
                        ).id,
                    }
                ),
                Command.create(
                    {
                        "sequence": 4,
                        "title": "Color",
                        "question_type": "numerical_box",
                        "res_partner_field": cls.env.ref(
                            "base.field_res_partner__color"
                        ).id,
                    }
                ),
                Command.create(
                    {
                        "sequence": 6,
                        "title": "Country",
                        "question_type": "simple_choice",
                        "res_partner_field": cls.env.ref(
                            "base.field_res_partner__country_id"
                        ).id,
                        "suggested_answer_ids": [
                            Command.create(
                                {
                                    "sequence": 1,
                                    "value": "Spain",
                                    "res_partner_field_resource_ref": (
                                        _create_reference(cls.env.ref("base.es"))
                                    ),
                                }
                            ),
                            Command.create(
                                {
                                    "sequence": 2,
                                    "value": "Romania",
                                    "res_partner_field_resource_ref": (
                                        _create_reference(cls.env.ref("base.ro"))
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
                        "res_partner_field": cls.env.ref(
                            "base.field_res_partner__category_id"
                        ).id,
                        "suggested_answer_ids": [
                            Command.create(
                                {
                                    "sequence": 1,
                                    "value": "Vendor",
                                    "res_partner_field_resource_ref": (
                                        _create_reference(cls.vendor_category)
                                    ),
                                }
                            ),
                            Command.create(
                                {
                                    "sequence": 2,
                                    "value": "Prospects",
                                    "res_partner_field_resource_ref": (
                                        _create_reference(cls.prospect_category)
                                    ),
                                }
                            ),
                            Command.create(
                                {
                                    "sequence": 3,
                                    "value": "Employees",
                                    "res_partner_field_resource_ref": (
                                        _create_reference(cls.employee_category)
                                    ),
                                }
                            ),
                        ],
                    }
                ),
            ],
        )
        questions_vals = questions_vals[0]
        cls.origin_survey = SurveySurvey.create(
            {
                "title": "Contact Creation Survey",
                "access_mode": "public",
                "users_can_go_back": True,
                "generate_contact": True,
                "create_parent_contact": True,
                "question_and_page_ids": list(questions_vals),
            }
        )
        survey_next_contact_q0 = survey_contact_q0.copy()
        survey_next_contact_q_company_name = survey_contact_q_company_name.copy()
        questions_vals[0] = Command.link(survey_next_contact_q_company_name.id)
        questions_vals[1] = Command.link(survey_next_contact_q0.id)
        questions_vals.append(
            Command.create(
                {
                    "sequence": 8,
                    "title": "Street",
                    "question_type": "char_box",
                    "res_partner_field": cls.env.ref(
                        "base.field_res_partner__street"
                    ).id,
                }
            ),
        )
        cls.next_survey = cls.origin_survey.copy(
            {"title": "Next contact survey", "question_and_page_ids": questions_vals}
        )
        cls.existing_inputs = cls.origin_survey.user_input_ids
        # Let's links several questions
        cls.origin_survey.next_survey_id = cls.next_survey
        survey_contact_q0.next_survey_question_id = survey_next_contact_q0.id
        survey_contact_q_company_name.next_survey_question_id = (
            survey_next_contact_q_company_name.id
        )

    def test_contact_generation(self):
        # Generate the contact first
        self.start_tour(
            f"/survey/start/{self.origin_survey.access_token}",
            "test_survey_contact_generation",
        )
        new_input = self.origin_survey.user_input_ids - self.existing_inputs
        partner = self.env["res.partner"].search(
            [("email", "=", "survey_contact_generation@test.com")]
        )
        self.assertEqual(partner.name, "My Name")
        self.assertEqual(partner.parent_id.name, "My Company Name")
        next_answer = new_input.next_survey_input_id
        self.start_tour(
            f"/survey/{self.next_survey.access_token}/{next_answer.access_token}",
            "test_survey_contact_update",
        )
        self.assertEqual(partner.name, "My Updated Name")
        self.assertEqual(partner.parent_id.name, "My Updated Company Name")
        self.assertEqual(partner.street, "Main Street, 42")
