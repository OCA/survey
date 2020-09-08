##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, fields, models


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    hidden = fields.Boolean(
        help=('Indicate whether this input\'s question was hidden on '
              'condition of earlier questions in the survey.'))

    @api.model
    def update_hidden(self, user_input, question, hidden=True):
        """ If hidden, delete all preexisting values and replace by a dummy
        one marked as hidden. If not hidden, delete any preexisting value
        marked as hidden. """
        domain = [
            ('user_input_id', '=', user_input.id),
            ('survey_id', '=', question.survey_id.id),
            ('question_id', '=', question.id)
        ]
        if not hidden:
            # Only select hidden values
            domain.append(('hidden', '=', True))
        existing = self.search(domain)
        if not hidden:
            if existing:
                # Remove the hidden value
                existing.unlink()
            return
        if existing:
            if len(existing) == 1 and existing.hidden:
                # Nothing to do
                return existing
            # Else, wipe all values
            existing.unlink()
        return self.create({
            'user_input_id': user_input.id,
            'question_id': question.id,
            'survey_id': question.survey_id.id,
            'skipped': True,
            'hidden': True,
        })

    @api.model
    def save_lines(self, user_input_id, question, post, answer_tag):
        """ Inject value for 'hidden' in context to be picked up in write and
        create methods """
        user_input = self.env['survey.user_input'].browse(user_input_id)
        hidden = question in user_input.get_hidden_questions()
        self.update_hidden(user_input, question, hidden=hidden)
        if hidden:
            return True
        return super(SurveyUserInputLine, self).save_lines(
            user_input_id, question, post, answer_tag)
