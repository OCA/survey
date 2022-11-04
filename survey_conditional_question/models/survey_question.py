##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"
    triggering_question_id = fields.Many2one(
        domain="""[('survey_id', '=', survey_id),
                         ('question_type', '!=', False), '|',
                     ('sequence', '<', sequence),
                     '&', ('sequence', '=', sequence), ('id', '<', id)]"""
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
        """Indicate that the question was hidden dynamically due to answers
        to questions on the same page
        """
        self.ensure_one()
        qkey = "{}_{}_{}".format(
            self.survey_id.id,
            self.page_id.id,
            self.triggering_question_id.id,
        )
        if qkey in post:
            # Compare the simple choice answer to the triggering answer
            return str(post[qkey]) != str(self.triggering_answer_id.id)
        akey = "{}_{}".format(qkey, self.triggering_answer_id.id)
        if any(key.startswith(qkey + "_") for key in post.keys()) and akey not in post:
            # Multiple choice answers for the triggering question are present,
            # but not this question's triggering answer
            return True
        return False
