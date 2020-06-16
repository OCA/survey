# Copyright 2020 Le Filament (<https://www.le-filament.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Survey Backend Readability",
    "summary": "Change survey creation workflow",
    "version": "12.0.1.0.0",
    "development_status": "Beta",
    "website": "https://github.com/OCA/survey",
    "author": "Le Filament, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["survey"],
    "data": [
        "views/survey_question_views.xml",
        "views/survey_survey_views.xml",
    ],
}
