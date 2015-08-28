# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class SurveyMailComposeMessage(models.TransientModel):
    _inherit = 'survey.mail.compose.message'

    tags = fields.Many2many(
        string='Add these tags to recipients',
        comodel_name='res.partner.category',
        relation='survey_mail_compose_message_res_partner_tag_rel',
        column1='wizard_id',
        column2='partner_tag_id',
    )
    partners_manual = fields.Many2many(
        string='Add these partners to recipients',
        comodel_name='res.partner',
        relation='survey_mail_compose_message_res_partner_manual_rel',
        column1='wizard_id',
        column2='partner_manual_id',
    )
    partner_ids = fields.Many2many(
        string='Recipients',
        readonly=True,
        compute='get_recipients'
    )

    @api.depends('tags', 'partners_manual')
    def get_recipients(self):
        """
        Populate the partner_ids field (Recipients) with all the partners
        added manually (in partners_manual) and the partners who have the
        tags chosen (in tags).
        Duplicates are avoided (we don't want partners to receive twice the
        same email because they have 2 tags interesting for us).
        This partner list is sorted by display_name.
        """
        self.partner_ids = self.partners_manual
        for tag in self.tags:
            self.partner_ids |= tag.partner_ids
        self.partner_ids = self.partner_ids.sorted(
            key=lambda p: p.display_name
        )
