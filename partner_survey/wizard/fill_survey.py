# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, models, fields


class FillSurvey(models.TransientModel):
    _name = 'fill.survey'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True)
    survey_id = fields.Many2one(
        comodel_name='survey.survey',
        string='Survey',
        required=True)

    @api.model
    def default_get(self, fields):
        res = super(FillSurvey, self).default_get(fields)
        active_id = self.env.context.get('active_id', False)
        active_model = self.env.context.get('active_model')
        if active_model == 'res.partner' and active_id:
            res.update({'partner_id': active_id})
        return res

    @api.multi
    def open_survey(self):
        self.ensure_one()
        user_input_obj = self.env['survey.user_input']
        survey_id = self.survey_id.id
        vals = {'survey_id': survey_id,
                'partner_id': self.partner_id.id}
        user_input = user_input_obj.create(vals)
        final_url = '/survey/fill/%s/%s' % (survey_id, user_input.token)
        return {'type': 'ir.actions.act_url',
                'url': final_url,
                'target': 'self', }
