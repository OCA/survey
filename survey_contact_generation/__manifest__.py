# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey contacts generation",
    "summary": "Generate new contacts from surveys",
    "version": "15.0.1.1.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["survey"],
    "data": [
        "views/survey_question_views.xml",
        "views/survey_survey_views.xml",
    ],
    "demo": ["demo/survey_contact_generation_demo.xml"],
    "assets": {
        "web.assets_tests": [
            "/survey_contact_generation/static/tests/survey_contact_generation_tour.js",
        ],
    },
}
