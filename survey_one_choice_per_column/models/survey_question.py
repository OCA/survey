# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, api, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    matrix_subtype = fields.Selection(
        selection_add=[('simple_restricted', 'One choice per column')]
    )

    @api.model
    def validate_question(self, question, post, answer_tag):
        if question.type == 'matrix' and \
           question.matrix_subtype == 'simple_restricted':
            return self.validate_simple_restricted_matrix(question, post,
                                                          answer_tag)
        return super(SurveyQuestion, self).validate_question(question, post,
                                                             answer_tag)

    def validate_simple_restricted_matrix(self, question, post, answer_tag):
        errors = {}
        answer_candidates = {key: post[key] for key in
                             filter(lambda key: key.startswith(answer_tag),
                                    post.keys())
                             }
        answer_number = len(answer_candidates)
        lines_number = len(question.labels_ids_2)
        if question.constr_mandatory and answer_number != lines_number:
            errors.update({answer_tag: question.constr_error_msg})
        values = answer_candidates.values()
        for answer in values:
            if len(filter(lambda i: i == answer, values)) > 1:
                errors.update({answer_tag: question.constr_error_msg})
        return errors
