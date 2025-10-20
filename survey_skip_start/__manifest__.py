# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey Skip Start",
    "summary": "Skip the surveys start screen and go directly to fill the form",
    "version": "17.0.1.0.2",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["pilarvargas-tecnativa"],
    "license": "AGPL-3",
    "depends": ["survey"],
    "data": [
        "views/survey_survey_views.xml",
    ],
    "assets": {
        "web.assets_tests": [
            "/survey_skip_start/static/tests/survey_skip_start_tour.esm.js",
        ],
    },
}
