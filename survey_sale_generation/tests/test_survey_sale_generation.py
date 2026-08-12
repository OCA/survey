# Copyright 2023 Tecnativa - David Vidal
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import HttpCase, new_test_user, tagged

from odoo.addons.survey.tests.common import SurveyCase


@tagged("-at_install", "post_install")
class SurveySaleGenerationCase(SurveyCase, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = new_test_user(cls.env, login="test-user", groups="base.group_portal")
        cls.support_hours = cls.env["product.product"].create(
            {
                "name": "Support hours",
                "type": "service",
                "list_price": 100,
            }
        )
        cls.gold_service = cls.env["product.product"].create(
            {
                "name": "Gold support",
                "type": "service",
                "list_price": 1000,
            }
        )
        cls.platinum_service = cls.env["product.product"].create(
            {
                "name": "Platinum support",
                "type": "service",
                "list_price": 10000,
            }
        )
        cls.silver_service = cls.env["product.product"].create(
            {
                "name": "Silver support",
                "type": "service",
                "list_price": 500,
            }
        )
        cls.dedicated_server = cls.env["product.product"].create(
            {
                "name": "Dedicated Server",
                "type": "service",
                "list_price": 500,
            }
        )
        cls.advanced_backup = cls.env["product.product"].create(
            {
                "name": "Advanced Backup",
                "type": "service",
                "list_price": 500,
            }
        )
        cls.mail_management = cls.env["product.product"].create(
            {
                "name": "Mail Management",
                "type": "service",
                "list_price": 500,
            }
        )
        cls.support_hiring_team = cls.env["crm.team"].create(
            {
                "name": "Support Hiring",
            }
        )
        cls.quotation_template_2 = cls.env["sale.order.template"].create(
            {
                "name": "Test order template 2",
            }
        )
        cls.quotation_template_3 = cls.env["sale.order.template"].create(
            {
                "name": "Test order template 3",
            }
        )
        cls.platinum_answer = cls.env["survey.question.answer"].create(
            {
                "sequence": 1,
                "value": "Platinum",
                "sale_order_template_id": cls.quotation_template_2.id,
                "product_ids": [
                    Command.link(cls.platinum_service.id),
                ],
            }
        )
        cls.gold_answer = cls.env["survey.question.answer"].create(
            {
                "sequence": 2,
                "value": "Gold",
                "sale_order_template_id": cls.quotation_template_3.id,
                "product_ids": [
                    Command.link(cls.gold_service.id),
                ],
            }
        )
        cls.question_3 = cls.env["survey.question"].create(
            {
                "sequence": 2,
                "title": "How many hours will you hire monthly?",
                "question_type": "numerical_box",
                "product_ids": [
                    Command.link(cls.support_hours.id),
                ],
                "constr_mandatory": True,
            }
        )
        cls.survey = cls.env["survey.survey"].create(
            {
                "title": "Hire Technical Support",
                "access_mode": "public",
                "generate_quotations": True,
                "crm_team_id": cls.support_hiring_team.id,
                "users_can_go_back": True,
                "question_and_page_ids": [
                    Command.create(
                        {
                            "sequence": 0,
                            "title": "Name",
                            "question_type": "char_box",
                            "show_in_sale_order_comment": True,
                            "constr_mandatory": True,
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 1,
                            "title": "E-mail address",
                            "question_type": "char_box",
                            "show_in_sale_order_comment": True,
                            "constr_mandatory": True,
                        }
                    ),
                    Command.link(cls.question_3.id),
                    Command.create(
                        {
                            "sequence": 3,
                            "title": "Choose your subscription level",
                            "question_type": "simple_choice",
                            "constr_mandatory": True,
                            "suggested_answer_ids": [
                                Command.link(cls.platinum_answer.id),
                                Command.link(cls.gold_answer.id),
                                Command.create(
                                    {
                                        "sequence": 3,
                                        "value": "Silver",
                                        "product_ids": [
                                            Command.link(cls.silver_service.id),
                                        ],
                                    }
                                ),
                            ],
                            "product_uom_qty_question_id": cls.question_3.id,
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 5,
                            "title": "Choose your extras",
                            "question_type": "multiple_choice",
                            "constr_mandatory": False,
                            "suggested_answer_ids": [
                                Command.create(
                                    {
                                        "sequence": 1,
                                        "value": "Dedicated Server",
                                        "product_ids": [
                                            Command.link(cls.dedicated_server.id),
                                        ],
                                    }
                                ),
                                Command.create(
                                    {
                                        "sequence": 2,
                                        "value": "Advanced Backup",
                                        "product_ids": [
                                            Command.link(cls.advanced_backup.id),
                                        ],
                                    }
                                ),
                                Command.create(
                                    {
                                        "sequence": 3,
                                        "value": "Mail Management",
                                        "product_ids": [
                                            Command.link(cls.mail_management.id),
                                        ],
                                    }
                                ),
                            ],
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 6,
                            "title": "Referenced by",
                            "question_type": "simple_choice",
                            "comments_allowed": True,
                            "comment_count_as_answer": True,
                            "comments_message": "Other:",
                            "sale_order_field": cls.env.ref(
                                "sale.field_sale_order__origin"
                            ).id,
                            "constr_mandatory": True,
                            "suggested_answer_ids": [
                                Command.create(
                                    {
                                        "sequence": 1,
                                        "value": "TV",
                                    }
                                ),
                                Command.create(
                                    {
                                        "sequence": 2,
                                        "value": "Internet",
                                    }
                                ),
                            ],
                        }
                    ),
                ],
            }
        )
        cls.quotation_template_1 = cls.env["sale.order.template"].create(
            {
                "name": "Test order template 1",
            }
        )
        cls.survey.sale_order_template_id = cls.quotation_template_1

    def test_sale_generation(self):
        initial_user_inputs = self.survey.user_input_ids
        # Run the survey as a portal user and get the generated quotation
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_sale_generation",
            login="test-user",
        )
        self.user_input = self.survey.user_input_ids - initial_user_inputs
        self.generated_sale = self.user_input.sale_order_id
        # Our generated sale should have these lines:

        # name              price_subtotal   product_uom_qty
        # --------------------------------------------------
        # Gold support            $1000.00             3.000
        # Advanced Backup          $500.00             1.000
        # Mail Management          $500.00             1.000
        # Support hours            $300.00             3.000
        expected_lines = {
            self.support_hours: 3.0,
            self.gold_service: 3.0,
            self.advanced_backup: 1.0,
            self.mail_management: 1.0,
        }
        resulting_lines = {
            line.product_id: line.product_uom_qty
            for line in self.generated_sale.order_line
        }
        self.assertEqual(resulting_lines, expected_lines)
        self.assertEqual(self.generated_sale.team_id, self.support_hiring_team)
        self.assertEqual(self.generated_sale.partner_id, self.user.partner_id)
        info_message, *_ = self.generated_sale.message_ids
        # Some other survey inputs can be annotated in the quotation chatter
        self.assertTrue("test@test.com" in info_message.body)
        self.assertEqual("Mr. Odoo", self.generated_sale.origin)
        self.assertEqual(
            self.generated_sale.sale_order_template_id,
            self.quotation_template_3,
            "The answer to the subscription level was gold, which had quotation "
            "template 3 as its value for the genarated sale",
        )

    def test_sale_quotation_no_template_in_answers(self):
        self.platinum_answer.write({"sale_order_template_id": False})
        self.gold_answer.write({"sale_order_template_id": False})
        initial_user_inputs = self.survey.user_input_ids
        self.start_tour(
            f"/survey/start/{self.survey.access_token}",
            "test_survey_sale_generation",
            login="test-user",
        )
        self.user_input = self.survey.user_input_ids - initial_user_inputs
        self.generated_sale = self.user_input.sale_order_id
        self.assertEqual(
            self.generated_sale.sale_order_template_id, self.quotation_template_1
        )
