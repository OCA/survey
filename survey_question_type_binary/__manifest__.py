# Copyright 2023 Jose Zambudio - Aures Tic <jose@aurestic.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Survey binary question type",
    "summary": """
        This module add binary field as question type for survey page""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Aures TIC, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "depends": ["survey"],
    "data": [
        "security/ir.model.access.csv",
        "views/survey_question.xml",
        "views/survey_user_input_line.xml",
        "templates/survey_template.xml",
    ],
    "assets": {
        "survey.survey_assets": [
            "/survey_question_type_binary/static/src/js/survey_form.js",
        ],
    },
}
