# Copyright 2026 Tecnativa - Eduardo Ezerouali
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSurveyContactNesting(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = cls.env["survey.survey"].create(
            {
                "title": "Nested Contact Creation Survey",
                "access_mode": "public",
                "users_can_go_back": True,
                "generate_contact": True,
            }
        )
        cls.questions = cls.env["survey.question"]
        cls.q_company = cls.questions.create(
            {
                "survey_id": cls.survey.id,
                "sequence": 0,
                "title": "Company name",
                "question_type": "char_box",
                "constr_mandatory": True,
                "res_partner_field": cls.env.ref("base.field_res_partner__name").id,
            }
        )
        cls.q_workcenter_1 = cls.questions.create(
            {
                "survey_id": cls.survey.id,
                "sequence": 1,
                "title": "Workcenter 1",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__name").id,
                "res_partner_type": "other",
            }
        )
        cls.q_workcenter_1_street = cls.questions.create(
            {
                "survey_id": cls.survey.id,
                "sequence": 2,
                "title": "Workcenter 1 street",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__street").id,
            }
        )
        cls.q_employee_1 = cls.questions.create(
            {
                "survey_id": cls.survey.id,
                "sequence": 3,
                "title": "Workcenter 1 employee",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__name").id,
            }
        )
        cls.q_employee_1_email = cls.questions.create(
            {
                "survey_id": cls.survey.id,
                "sequence": 4,
                "title": "Workcenter 1 employee email",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__email").id,
            }
        )
        cls.q_workcenter_2 = cls.questions.create(
            {
                "survey_id": cls.survey.id,
                "sequence": 5,
                "title": "Workcenter 2",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__name").id,
                "res_partner_type": "other",
            }
        )
        cls.q_workcenter_2_street = cls.questions.create(
            {
                "survey_id": cls.survey.id,
                "sequence": 6,
                "title": "Workcenter 2 street",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__street").id,
            }
        )
        cls.q_employee_2 = cls.questions.create(
            {
                "survey_id": cls.survey.id,
                "sequence": 7,
                "title": "Workcenter 2 employee",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__name").id,
            }
        )
        questions = {
            question.sequence: question for question in cls.survey.question_ids
        }
        questions[1].survey_question_node_id = questions[0]
        questions[2].survey_question_node_id = questions[1]
        questions[3].survey_question_node_id = questions[1]
        questions[4].survey_question_node_id = questions[3]
        questions[5].survey_question_node_id = questions[0]
        questions[6].survey_question_node_id = questions[5]
        questions[7].survey_question_node_id = questions[5]

    def _answer(self, user_input, answers):
        """Answer the given `{question: value}` map with char box lines"""
        for question, value in answers.items():
            self.env["survey.user_input.line"].create(
                {
                    "user_input_id": user_input.id,
                    "question_id": question.id,
                    "skipped": not value,
                    "answer_type": "char_box" if value else False,
                    "value_char_box": value,
                }
            )

    def _submit(self, answers=None):
        """Answer the whole survey, overriding the given answers, and submit it"""
        user_input = self.env["survey.user_input"].create({"survey_id": self.survey.id})
        default_answers = {
            self.q_company: "ACME",
            self.q_workcenter_1: "Workcenter North",
            self.q_workcenter_1_street: "1 North Street",
            self.q_employee_1: "Alice",
            self.q_employee_1_email: "alice@example.com",
            self.q_workcenter_2: "Workcenter South",
            self.q_workcenter_2_street: "2 South Street",
            self.q_employee_2: "Bob",
        }
        default_answers.update(answers or {})
        self._answer(user_input, default_answers)
        user_input._mark_done()
        return user_input

    def _get_contact(self, user_input, name):
        return self.env["res.partner"].search(
            [("id", "child_of", user_input.partner_id.id), ("name", "=", name)]
        )

    def test_groups_open_one_contact_per_name_question(self):
        """A name question opens a contact, any other one fills the node's contact"""
        user_input = self.env["survey.user_input"].create({"survey_id": self.survey.id})
        self._answer(
            user_input,
            {
                self.q_company: "ACME",
                self.q_workcenter_1: "Workcenter North",
                self.q_workcenter_1_street: "1 North Street",
                self.q_employee_1: "Alice",
            },
        )
        groups = user_input._get_partner_groups()
        self.assertEqual(
            {key.title for key in groups},
            {"Company name", "Workcenter 1", "Workcenter 1 employee"},
        )
        # The street doesn't open a contact: it fills in the workcenter's one
        self.assertEqual(
            groups[self.q_workcenter_1].question_id,
            self.q_workcenter_1 + self.q_workcenter_1_street,
        )

    def test_contact_hierarchy(self):
        """Every node generates a contact hanging from the contact of its node"""
        user_input = self._submit()
        company = user_input.partner_id
        self.assertEqual(company.name, "ACME")
        self.assertFalse(company.parent_id)
        self.assertEqual(company.generating_survey_user_input_id, user_input)
        north = self._get_contact(user_input, "Workcenter North")
        south = self._get_contact(user_input, "Workcenter South")
        self.assertEqual(north.parent_id, company)
        self.assertEqual(south.parent_id, company)
        self.assertEqual(self._get_contact(user_input, "Alice").parent_id, north)
        self.assertEqual(self._get_contact(user_input, "Bob").parent_id, south)

    def test_sibling_nodes_do_not_share_their_answers(self):
        """Contacts hanging from the same node don't overwrite each other"""
        user_input = self._submit()
        self.assertEqual(
            self._get_contact(user_input, "Workcenter North").street, "1 North Street"
        )
        self.assertEqual(
            self._get_contact(user_input, "Workcenter South").street, "2 South Street"
        )
        self.assertEqual(
            self._get_contact(user_input, "Alice").email, "alice@example.com"
        )
        self.assertFalse(self._get_contact(user_input, "Bob").email)

    def test_address_type_isolates_the_address(self):
        """A node typed as an address doesn't share it with its parent's family"""
        user_input = self._submit()
        north = self._get_contact(user_input, "Workcenter North")
        self.assertEqual(north.type, "other")
        # A `contact` child still shares the address of its own node
        self.assertEqual(self._get_contact(user_input, "Alice").type, "contact")
        self.assertEqual(self._get_contact(user_input, "Alice").street, north.street)

    def test_skipped_node_hands_its_children_over(self):
        """A node whose name went unanswered generates no contact"""
        user_input = self._submit({self.q_workcenter_1: False})
        company = user_input.partner_id
        self.assertFalse(self._get_contact(user_input, "Workcenter North"))
        # Alice hangs from the company now, as her own node generated nothing
        self.assertEqual(self._get_contact(user_input, "Alice").parent_id, company)
        # A nameless contact holding the orphan street is not generated either
        contacts = self.env["res.partner"].search([("id", "child_of", company.id)])
        self.assertFalse(contacts.filtered(lambda x: not x.name))
        self.assertFalse(contacts.filtered(lambda x: x.street == "1 North Street"))

    def test_root_node_contact_is_the_generated_one(self):
        """With every answer inside a node there's no main contact to generate"""
        user_input = self._submit()
        # The root node contact takes the place of the main one
        self.assertEqual(user_input.partner_id.name, "ACME")
        self.assertEqual(
            self.env["res.partner"].search_count(
                [("generating_survey_user_input_id", "=", user_input.id)]
            ),
            1,
        )
