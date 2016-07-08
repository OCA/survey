# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, api, models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input_line"
    
    #TODO: API2, overridden method is API1
    def save_line_matrix(self, cr, uid, user_input_id, question, post, answer_tag, context=None):
        vals = {
            'user_input_id': user_input_id,
            'question_id': question.id,
            'page_id': question.page_id.id,
            'survey_id': question.survey_id.id,
            'skipped': False
        }
        old_uil = self.search(cr, uid, [('user_input_id', '=', user_input_id),
                                        ('survey_id', '=', question.survey_id.id),
                                        ('question_id', '=', question.id)],
                              context=context)
        if old_uil:
            self.unlink(cr, uid, old_uil, context=context)

        no_answers = True
        ca = dict_keys_startswith(post, answer_tag)

        comment_answer = ca.pop(("%s_%s" % (answer_tag, 'comment')), '').strip()
        if comment_answer:
            vals.update({'answer_type': 'text', 'value_text': comment_answer})
            self.create(cr, uid, vals, context=context)
            no_answers = False

        if question.matrix_subtype == 'simple' or question.matrix_subtype == 'simple_restricted':
            for row in question.labels_ids_2:
                a_tag = "%s_%s" % (answer_tag, row.id)
                if a_tag in ca:
                    no_answers = False
                    vals.update({'answer_type': 'suggestion', 'value_suggested': ca[a_tag], 'value_suggested_row': row.id})
                    self.create(cr, uid, vals, context=context)

        elif question.matrix_subtype == 'multiple':
            for col in question.labels_ids:
                for row in question.labels_ids_2:
                    a_tag = "%s_%s_%s" % (answer_tag, row.id, col.id)
                    if a_tag in ca:
                        no_answers = False
                        vals.update({'answer_type': 'suggestion', 'value_suggested': col.id, 'value_suggested_row': row.id})
                        self.create(cr, uid, vals, context=context)
        if no_answers:
            vals.update({'answer_type': None, 'skipped': True})
            self.create(cr, uid, vals, context=context)
        return True
    
def dict_keys_startswith(dictionary, string):
    '''Returns a dictionary containing the elements of <dict> whose keys start
    with <string>.

    .. note::
        This function uses dictionary comprehensions (Python >= 2.7)'''
    return {k: dictionary[k] for k in filter(lambda key: key.startswith(string), dictionary.keys())}