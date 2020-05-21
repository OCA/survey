# -*- coding: utf-8 -*-
# Nicolas Trubert
{
    'name': 'Survey Partner Tag Share',
    'version': '12.0.0',
    'category': 'Marketing',
    'summary': 'Share a survey to all the partners that have a given tag',
    'author':'Nicolas Trubert',
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
    'auto_install': False,
}
