# Copyright 2020 Le Filament (<https://le-filament.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Survey description field",
    "summary": """
               Displays description and thank you fields for survey,
               page and question.
               """,
    "version": "14.0.1.0.0",
    # This module should not be migrated to 15.0.
    "development_status": "Beta",
    "website": "https://github.com/OCA/survey",
    "author": "Le Filament, Odoo Community Association (OCA)",
    "maintainers": ["remi-filament"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["survey"],
    "data": ["views/survey_views.xml"],
}
