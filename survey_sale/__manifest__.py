# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Survey Sale",
    "summary": """
        This addon allows to create surveys from sale orders""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "depends": ["survey_link_base", "sale_management"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
    ],
    "maintainers": ["adasatorres"],
}
