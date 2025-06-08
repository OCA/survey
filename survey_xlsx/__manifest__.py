# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Survey XLSX",
    "summary": """
        XLSX Report to show the survey results""",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "author": "Creu Blanca, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "depends": ["survey", "report_xlsx"],
    "data": ["report/report_survey_xlsx.xml"],
}
