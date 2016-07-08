# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, api, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"
    
    matrix_subtype = fields.Selection(selection_add=[('simple_restricted', 'One choice per column')])
    
    #TODO: API2, overridden method is API1
    def validate_matrix(self, cr, uid, question, post, answer_tag, context=None):
        errors = {}
        
        #Requirement test
        if question.constr_mandatory:
            lines_number = len(question.labels_ids_2)
            answer_candidates = dict_keys_startswith(post, answer_tag)
            
            # Number of lines that have been answered
            if question.matrix_subtype == 'simple' or question.matrix_subtype == 'simple_restricted':
                answer_number = len(answer_candidates)
            elif question.matrix_subtype == 'multiple':
                answer_number = len(set([sk.rsplit('_', 1)[0] for sk in answer_candidates.keys()]))
            # Validate that each line has been answered
            if answer_number != lines_number:
                errors.update({answer_tag: question.constr_error_msg})
        
        #Simple restricted unique answer test
        if(question.matrix_subtype == 'simple_restricted'):
            answer_candidates = dict_keys_startswith(post, answer_tag)
            for answer_candidate in answer_candidates:
                if(len(dict_keys_startswith(answer_candidates, answer_tag + "_" + answer_candidate)) > 1):
                    errors.update({answer_tag: question.constr_error_msg})
            
        return errors