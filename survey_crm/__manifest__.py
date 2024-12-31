# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Survey CRM",
    "summary": """
        This addon allows to create surveys from CRM leads""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "depends": ["survey_link_base", "crm"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/crm_lead_views.xml",
    ],
    "maintainers": ["szalatyzuzanna"],
}
