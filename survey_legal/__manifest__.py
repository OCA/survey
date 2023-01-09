# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey legal terms",
    "summary": "Require legal terms before survey submit",
    "version": "13.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["survey", "website_legal_page"],
    "data": [
        "views/survey_views.xml",
        "views/survey_templates.xml",
        "views/survey_user_input_views.xml",
    ],
}
