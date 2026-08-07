# Copyright 2025 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey model selection question type",
    "version": "19.0.1.0.0",
    "summary": "This module add model selection field as question type for survey page",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "license": "AGPL-3",
    "maintainers": ["eduezerouali-tecnativa"],
    "category": "Marketing/Survey",
    "depends": ["survey"],
    "data": [
        "security/ir.model.access.csv",
        "views/survey_question_views.xml",
        "views/survey_user_input_line_views.xml",
        "views/survey_template.xml",
    ],
    "assets": {
        "survey.survey_assets": [
            "survey_question_type_model_selection/static/src/js/survey_form.esm.js",
            "survey_question_type_model_selection/static/src/lib/choices/choices.js",
            "survey_question_type_model_selection/static/src/lib/choices/choices.css",
        ],
        "web.assets_tests": [
            "survey_question_type_model_selection/static/tests/test_tour_survey_question_model.esm.js",
        ],
    },
}
