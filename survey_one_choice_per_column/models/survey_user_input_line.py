# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input_line"

    @api.model
    def save_lines(self, user_input_id, question, post, answer_tag):
        if question.type == 'matrix' and \
           question.matrix_subtype == 'simple_restricted':
            return self.save_line_simple_restricted_matrix(user_input_id,
                                                           question, post,
                                                           answer_tag)
        return super(SurveyUserInputLine, self).save_lines(user_input_id,
                                                           question, post,
                                                           answer_tag)

    def save_line_simple_restricted_matrix(self, user_input_id, question, post,
                                           answer_tag):
        vals = {
            'user_input_id': user_input_id,
            'question_id': question.id,
            'page_id': question.page_id.id,
            'survey_id': question.survey_id.id,
            'skipped': False
        }
        candidates = {key: post[key] for key in
                      filter(lambda key: key.startswith(answer_tag),
                             post.keys())
                      }
        no_answers = True
        for row in question.labels_ids_2:
            tag = "%s_%s" % (answer_tag, row.id)
            if tag in candidates:
                no_answers = False
                vals.update({'answer_type': 'suggestion',
                             'value_suggested': candidates[tag],
                             'value_suggested_row': row.id
                             })
                self.create(vals)
        if no_answers:
            vals.update({'answer_type': None, 'skipped': True})
            self.create(vals)
        return True
