# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# Part of ForgeFlow. See LICENSE file for full copyright and licensing details.

{
    "name": "Survey Question Group",
    "version": "16.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "license": "AGPL-3",
    "category": "Marketing/Surveys",
    "summary": "Group reusable template questions and add them to surveys",
    "depends": [
        "survey",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/survey_add_question_group_wizard_views.xml",
        "views/survey_question_group_views.xml",
        "views/survey_survey_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
