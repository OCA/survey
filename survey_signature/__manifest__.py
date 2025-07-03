# Copyright 2025 Binhex - Zuzanna Elżbieta Szalaty Szalaty
# Copyright 2025 Binhex - Adasat Torres de Leon
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Survey Signature",
    "summary": """
        This addon adds a new question type to surveys.
        """,
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "category": "Survey",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["survey"],
    "data": [
        "views/survey_question_views.xml",
        "views/survey_user_input_line.xml",
        "views/survey_templates.xml",
        "views/survey_templates_print.xml",
    ],
    "assets": {
        "survey.survey_assets": [
            "survey_signature/static/src/js/*.js",
        ]
    },
}
