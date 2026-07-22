# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey contacts generation for model selection",
    "summary": "Generate new contacts from surveys using model selection",
    "version": "17.0.1.0.0",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["eduezerouali-tecnativa"],
    "license": "AGPL-3",
    "depends": ["survey_contact_generation", "survey_question_type_model_selection"],
    "assest": {
        "web.assets_tests": [
            "survey_contact_generation_model_selection/static/tests/test_tour_contact_generation_model_selection.esm.js",
        ],
    },
    "auto_install": True,
}
