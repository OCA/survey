# Copyright 2026 elego Software Solutions GmbH - Laya Rabasa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSurveyContactFields(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = cls.env["survey.survey"].create(
            {"title": "Contact fields", "generate_contact": True}
        )
        cls.field_name = cls.env.ref("base.field_res_partner__name")
        cls.field_function = cls.env.ref("base.field_res_partner__function")
        cls.field_ref = cls.env.ref("base.field_res_partner__ref")
        cls.field_country = cls.env.ref("base.field_res_partner__country_id")
        cls.q_name = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Name",
                "question_type": "char_box",
                "res_partner_field": cls.field_name.id,
            }
        )
        cls.q_function = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Job position",
                "question_type": "simple_choice",
                "res_partner_field": cls.field_function.id,
                "suggested_answer_ids": [
                    (0, 0, {"value": "Manager"}),
                    (0, 0, {"value": "Developer"}),
                ],
            }
        )
        cls.q_ref = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Reference",
                "question_type": "multiple_choice",
                "res_partner_field": cls.field_ref.id,
                "suggested_answer_ids": [
                    (0, 0, {"value": "A"}),
                    (0, 0, {"value": "B"}),
                ],
            }
        )
        cls.q_email = cls.env["survey.question"].create(
            {
                "survey_id": cls.survey.id,
                "title": "Email",
                "question_type": "char_box",
                "res_partner_field": cls.env.ref("base.field_res_partner__email").id,
            }
        )

    def _answer_char(self, user_input, question, value):
        """Answer a char box question with the given value"""
        self.env["survey.user_input.line"].create(
            {
                "user_input_id": user_input.id,
                "question_id": question.id,
                "answer_type": "char_box",
                "value_char_box": value,
            }
        )

    def _answer_choice(self, user_input, question, value):
        """Answer a choice question with the suggested answer of the given value"""
        self.env["survey.user_input.line"].create(
            {
                "user_input_id": user_input.id,
                "question_id": question.id,
                "answer_type": "suggestion",
                "suggested_answer_id": question.suggested_answer_ids.filtered(
                    lambda x: x.value == value
                ).id,
            }
        )

    def test_allowed_partner_field_domain(self):
        """Each question type can only be mapped to compatible contact fields"""
        self.assertIn(
            ("ttype", "in", ["char", "text"]),
            self.q_name.allowed_partner_field_domain,
        )
        self.assertIn(
            ("ttype", "in", ["many2many", "html", "char"]),
            self.q_ref.allowed_partner_field_domain,
        )

    def test_answer_default_get_relational_field(self):
        """Relational contact fields suggest a record for the answer"""
        vals = (
            self.env["survey.question.answer"]
            .with_context(default_res_partner_field=self.field_country.id)
            .default_get(["res_partner_field", "res_partner_field_resource_ref"])
        )
        country = self.env["res.country"].search([], limit=1)
        self.assertEqual(
            vals["res_partner_field_resource_ref"], f"res.country,{country.id}"
        )

    def test_answer_default_get_plain_field(self):
        """Plain contact fields just use the answer value"""
        vals = (
            self.env["survey.question.answer"]
            .with_context(default_res_partner_field=self.field_function.id)
            .default_get(["res_partner_field", "res_partner_field_resource_ref"])
        )
        self.assertFalse(vals.get("res_partner_field_resource_ref"))

    def test_answer_value_from_resource_ref(self):
        """Picking a record for the answer sets its name as the answer value"""
        country = self.env.ref("base.es")
        answer = self.q_function.suggested_answer_ids[0]
        answer.res_partner_field_resource_ref = f"res.country,{country.id}"
        answer._onchange_res_partner_field_resource_ref()
        self.assertEqual(answer.value, country.display_name)

    def test_answer_value_kept_without_resource_ref(self):
        """Without a picked record the answer value is left as it is"""
        answer = self.q_function.suggested_answer_ids[0]
        answer._onchange_res_partner_field_resource_ref()
        self.assertEqual(answer.value, "Manager")

    def test_existing_contact_matched_by_email(self):
        """An answer with the email of an existing contact is linked to it"""
        partner = self.env["res.partner"].create(
            {"name": "Juanito Existing", "email": "juanito@example.com"}
        )
        user_input = self.env["survey.user_input"].create({"survey_id": self.survey.id})
        self._answer_char(user_input, self.q_name, "Juanito")
        self._answer_char(user_input, self.q_email, "juanito@example.com")
        user_input._mark_done()
        self.assertEqual(user_input.partner_id, partner)
        self.assertFalse(
            self.env["res.partner"].search([("name", "=", "Juanito")]),
            "No duplicate contact should be created",
        )

    def test_no_contact_without_contact_answers(self):
        """No contact is generated when no contact question was answered"""
        user_input = self.env["survey.user_input"].create({"survey_id": self.survey.id})
        user_input._mark_done()
        self.assertFalse(user_input.partner_id)

    def test_choice_answers_fill_char_fields(self):
        """Choice answers mapped to char fields store the chosen values"""
        user_input = self.env["survey.user_input"].create({"survey_id": self.survey.id})
        self._answer_char(user_input, self.q_name, "Juanito")
        self._answer_choice(user_input, self.q_function, "Manager")
        self._answer_choice(user_input, self.q_ref, "A")
        self._answer_choice(user_input, self.q_ref, "B")
        user_input._mark_done()
        partner = user_input.partner_id
        self.assertEqual(partner.name, "Juanito")
        self.assertEqual(partner.function, "Manager")
        # Multiple choice answers are concatenated
        self.assertEqual(partner.ref, "AB")
