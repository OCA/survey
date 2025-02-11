# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey Certification Sending",
    "summary": "Controls the automatic sending of certifications in surveys.",
    "version": "15.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "maintainers": ["pilarvargas-tecnativa"],
    "license": "AGPL-3",
    "depends": ["survey"],
    "data": [
        "views/survey_survey_views.xml",
        "views/survey_templates.xml",
        "views/survey_user_views.xml",
    ],
    "installable": True,
}
