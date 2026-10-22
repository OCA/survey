# Copyright 2026 Acsone
# @author Pierre Verkest <pierre.verkest@apycod.fr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
{
    "name": "Survey user input edit",
    "summary": "Allow respondents to modify their submitted survey responses",
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Pierre Verkest, Odoo Community Association (OCA)",
    "maintainers": ["petrus-v"],
    "license": "LGPL-3",
    "depends": [
        "survey",
        "survey_prevent_create_on_start",
    ],
    "data": [
        "views/survey_survey_views.xml",
        "views/survey_templates.xml",
    ],
    "assets": {
        "web.assets_tests": [
            "survey_user_input_edit/static/tests/tours/*.js",
        ],
    },
    "installable": True,
}
