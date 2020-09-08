##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    @api.model
    def next_page(self, user_input, page_id, go_back=False):
        """ Skip pages that only have hidden questions on them,
        except if its the last page or the first page (in which case there
        is a configuration error in the survey). """
        questions_to_hide = user_input.get_hidden_questions()
        res = super(SurveySurvey, self).next_page(
            user_input, page_id, go_back=go_back)
        page, index, last = res
        if page and not (page.question_ids - questions_to_hide):
            if (not go_back and not last) or (go_back and index):
                # Mark every question on this hidden page as hidden.
                for question in page.question_ids:
                    self.env['survey.user_input_line'].update_hidden(
                        user_input, question)
                return self.next_page(
                    user_input, page.id, go_back=go_back)
        return res
