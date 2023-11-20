# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey Result Mail",
    "summary": "Send survey answers to the survey user",
    "version": "15.0.1.1.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["survey"],
    "data": [
        "templates/survey_answer_templates.xml",
        "reports/survey_answer_report.xml",
        "data/mail_template.xml",
        "views/survey_survey_views.xml",
        "views/survey_user_input_views.xml",
    ],
}
