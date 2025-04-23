# Copyright 2025 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Survey Certification Branding",
    "summary": (
        "This module enables customization of certification reports by allowing "
        "a custom logo and company name per certification."
    ),
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Binhex,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "depends": ["survey"],
    "data": [
        "views/survey_survey_views.xml",
        "report/survey_report_templates.xml",
    ],
}
