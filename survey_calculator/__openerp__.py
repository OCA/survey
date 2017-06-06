# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Survey Calculator',
    'version': '8.0.1.0.0',
    'category': 'Marketing',
    'summary': 'Compute calculations from answers given to a survey',
    'author': 'Savoir-faire Linux, Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'depends': [
        'survey',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/survey_calculator_computation.xml',
        'views/survey_calculator_result.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
