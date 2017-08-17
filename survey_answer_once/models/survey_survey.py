# -*- coding: utf-8 -*-
import logging

from openerp import SUPERUSER_ID, fields, models, api, _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Survey(models.Model):
    _inherit = 'survey.survey'

    allow_duplicates = fields.Boolean(
        "Allow users to give multiple Responses",
        default=True
    )


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    @api.model
    def create(self, vals):
        partner_id = self.env.user.partner_id.id
        question_id = vals.get('question_id')
        survey = self.env['survey.survey'].browse(vals.get('survey_id'))
        user_input = self.env['survey.user_input'].browse(
            vals.get('user_input_id'))
        _logger.info(
            _("User '%s' (%d, partner %d) filled survey %d question %d"),
            self.env.user.name,
            self.env.uid,
            partner_id,
            survey.id,
            question_id
        )
        if survey.allow_duplicates:
            _logger.info(
                _('Allowing, because survey allows duplicate answers'))
        else:
            if self.env.uid == SUPERUSER_ID:
                alt_partner_id = user_input.partner_id.id
                if alt_partner_id and alt_partner_id != partner_id:
                    partner_id = alt_partner_id
                    _logger.info(
                        _("User input object says partner id is %d"),
                        partner_id
                    )
                else:
                    _logger.info(
                        _('Disallowing, because we cannot check duplicates.'))
                    raise ValidationError(_('disallow_invite'))
            existing = self.env['survey.user_input_line'].search([
                ('question_id', '=', question_id),
                ('user_input_id.partner_id', '=', partner_id)
            ])
            if not existing:
                _logger.info(
                    _('Allowing, because we found no existing answers.'))
            else:
                _logger.info(
                    _('Disallowing, because we found existing answers.'))
                raise ValidationError(_('duplicate_answer'))
        return super(SurveyUserInputLine, self).create(vals)
