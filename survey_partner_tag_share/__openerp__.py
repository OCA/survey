# -*- coding: utf-8 -*-
# Copyright 2016 Savoirfairelinux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Survey Partner Tag Share',
    'version': '8.0.1.0.0',
    'category': 'Marketing',
    'summary': 'Share a survey to all the partners that have a given tag',
    'author': 'Savoir-faire Linux, Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'depends': [
        'survey',
    ],
    'data': [
        'wizard/survey_email_compose_message.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
