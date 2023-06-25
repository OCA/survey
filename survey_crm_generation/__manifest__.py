# Copyright 2023 Tecnativa - David Vidal
# Copyright 2023 Technaureus - Sreejishnu E
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey leads generation",
    "summary": "Generate CRM leads/opportunities from surveys",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa,"
    "Technaureus,"          
    "Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["survey", "crm"],
    "data": [
        "views/survey_survey_views.xml",
        "views/survey_question_views.xml",
        "views/survey_user_input_views.xml",
        "views/crm_lead_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/survey_crm_generation/static/tests/survey_crm_generation_tour.js",
        ],
    },
    "demo": ["demo/survey_crm_demo.xml"],
}
