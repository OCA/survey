# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey CRM generation for model selection",
    "summary": "Generate new leads from surveys using model selection",
    "version": "19.0.1.0.0",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["eduezerouali-tecnativa"],
    "license": "AGPL-3",
    "depends": ["survey_crm_generation", "survey_question_type_model_selection"],
    "assets": {
        "web.assets_tests": [
            "survey_crm_generation_model_selection/static/tests/tour_crm_generation_model.esm.js"
        ],
    },
    "auto_install": True,
}
