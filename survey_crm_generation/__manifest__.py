# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey leads generation",
    "summary": "Generate CRM leads/opportunities from surveys",
    "version": "15.0.1.1.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["survey_result_mail", "crm"],
    "data": [
        "views/survey_survey_views.xml",
        "views/survey_question_views.xml",
        "views/survey_user_input_views.xml",
        "views/crm_lead_views.xml",
    ],
    "demo": ["demo/survey_crm_demo.xml"],
    "assets": {
        "web.assets_tests": [
            "/survey_crm_generation/static/tests/survey_crm_generation_tour.js",
        ],
    },
}
