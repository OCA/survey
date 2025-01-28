# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey Partner Representative",
    "summary": "Fill the survey on behalf of others",
    "version": "17.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["survey"],
    "data": [
        "security/survey_partner_representative_security.xml",
        "views/survey_survey_views.xml",
        "views/survey_user_input_views.xml",
    ],
    "demo": ["demo/survey_partner_representative_demo.xml"],
    "assets": {
        "web.assets_tests": [
            "/survey_partner_representative/static/tests/survey_representative_tour.esm.js",
        ],
    },
}
