# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class SurveyMailComposeMessage(models.TransientModel):
    _inherit = 'survey.mail.compose.message'

    tag_ids = fields.Many2many(
        'res.partner.category',
        'survey_mail_compose_message_res_partner_tag_rel',
        'wizard_id',
        'partner_tag_id',
        string='Add these tags to recipients',
    )
    partners_manual = fields.Many2many(
        'res.partner',
        'survey_mail_compose_message_res_partner_manual_rel',
        'wizard_id',
        'partner_manual_id',
        string='Add these partners to recipients',
    )
    partner_ids = fields.Many2many(
        string='Recipients',
        readonly=True,
        compute='get_recipients'
    )

    @api.depends('tag_ids', 'partners_manual')
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
        for tag in self.tag_ids:
            self.partner_ids |= tag.partner_ids
        self.partner_ids = self.partner_ids.sorted(
            key=lambda p: p.display_name
        )
