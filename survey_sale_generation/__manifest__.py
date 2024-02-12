# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey sale generation",
    "summary": "Generate sale orders from surveys",
    "version": "15.0.2.1.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["survey_result_mail", "sale_management"],
    "data": [
        "views/survey_question_views.xml",
        "views/survey_survey_views.xml",
        "views/survey_user_input_views.xml",
        "views/sale_order_views.xml",
    ],
    "demo": ["demo/survey_sale_demo.xml"],
    "assets": {
        "web.assets_tests": [
            "/survey_sale_generation/static/tests/survey_sale_generation_tour.js",
        ],
    },
}
