# Copyright 2025 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Survey Previous Page Skip Validation",
    "summary": """
        This addon allows users to return to the previous
        page without answering the mandatory questions.
        .""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "depends": ["survey"],
    "assets": {
        "survey.survey_assets": [
            "survey_previous_page_skip_validation/static/src/js/*.js"
        ]
    },
    "maintainers": ["adasatorres"],
}
