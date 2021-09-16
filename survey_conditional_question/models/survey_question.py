##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    # Don't copy conditional fields. It could lead to references to a
    # different survey if a survey was copied.
    is_conditional = fields.Boolean("Conditional Question", copy=False,)
    triggering_question_id = fields.Many2one(
        comodel_name="survey.question",
        string="Condition Question",
        help="The question which determines if this question is shown",
        copy=False,
    )
    triggering_answer_id = fields.Many2one(
        comodel_name="survey.label",
        string="Condition Option",
        help="The option which determines if this question is shown",
        copy=False,
    )
    triggering_question_type = fields.Selection(
        related="triggering_question_id.question_type",
        string="Triggering question type",
    )
    conditional_minimum_value = fields.Float(
        help="If the value is lower, it will not be shown", copy=False
    )
    conditional_maximum_value = fields.Float(
        help="If the value is higher, it will not be shown", copy=False
    )

    def _hidden_on_same_page(self, post):
        """ Indicate that the question was hidden dynamically due to answers
        to questions on the same page
        """
        self.ensure_one()
        question = self.triggering_question_id
        qkey = "{}_{}".format(self.survey_id.id, question.id,)
        if qkey in post and self.triggering_question_type == "simple_choice":
            # Compare the simple choice answer to the triggering answer
            return str(post[qkey]) != str(self.triggering_answer_id.id)
        akey = "{}_{}".format(qkey, self.triggering_answer_id.id)
        if (
            any(key.startswith(qkey + "_") for key in post.keys())
            and akey not in post
            and self.triggering_question_type == "multiple_choice"
        ):
            # Multiple choice answers for the triggering question are present,
            # but not this question's triggering answer
            return True
        if qkey in post and (
            float(post[qkey]) < question.conditional_minimum_value
            or float(post[qkey]) > question.conditional_maximum_value
        ):
            return True
        return False

    def validate_question(self, post, answer_tag):
        """ Skip validation of hidden questions """
        self.ensure_one()
        if self.is_conditional and self.triggering_question_id:
            if self.page_id == self.triggering_question_id.page_id:
                if self._hidden_on_same_page(post):
                    return {}
            else:
                # In case the dependent question was on a previous page
                input_answer_ids = self.env["survey.user_input_line"].search(
                    [
                        ("user_input_id.token", "=", post.get("token")),
                        ("question_id", "=", self.triggering_question_id.id),
                    ]
                )
                value = input_answer_ids.mapped("value_suggested")
                if (
                    self.triggering_question_type
                    in ["simple_choice", "multiple_choice"]
                    and self.triggering_answer_id not in value
                ):
                    return {}
                if (
                    self.triggering_question_type in ["numerical_box"]
                    and self.triggering_answer_id not in value
                    or (
                        value <= self.conditional_minimum_value
                        or value >= self.conditional_maximum_value
                    )
                ):
                    return {}
        return super(SurveyQuestion, self).validate_question(post, answer_tag)
