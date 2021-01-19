# Copyright 2020 Le Filament (<https://le-filament.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey description field",
    "summary": """
               Displays description and thank you fields for survey,
               page and question""",
    "version": "12.0.1.0.1",
    "development_status": "Beta",
    "website": "https://github.com/OCA/survey.git",
    "author": "Le Filament, Odoo Community Association (OCA)",
    "maintainers": ["remi-filament"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "survey",
    ],
    "data": [
        "views/survey_views.xml",
    ],
}
