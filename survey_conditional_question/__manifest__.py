# Copyright 2020 Le Filament (<https://www.le-filament.com>)
# License GPL-3.0 or later (https://www.gnu.org/licenses/gpl).

{
    "name": "Survey Conditional Question",
    "summary": "Display question depending on answer to previous one",
    "version": "13.0.1.0.0",
    "development_status": "Beta",
    "website": "https://github.com/OCA/survey",
    "author": "Le Filament, Vuente, Creu Blanca, Odoo Community Association (OCA)",
    "license": "GPL-3",
    "application": False,
    "installable": True,
    "depends": ["survey"],
    "data": [
        "views/survey_question_views.xml",
        "templates/survey_extra_templates.xml",
    ],
}
