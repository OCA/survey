# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Survey One Choice Per Column',
    'category': 'Marketing',
    'version': '9.0.1.0.0',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'depends': [
        'web_editor',
        'survey'
    ],
    'data': [
        'views/assets.xml',
        'views/survey_one_choice_per_column_templates.xml',
    ],
    'summary': "Adds a new option 'One Choice Per Column' to matrix types."
}
