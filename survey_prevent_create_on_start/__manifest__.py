# Copyright 2026 Acsone
# @author Pierre Verkest <pierre.verkest@apycod.fr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    "name": "Survey Prevent Create on Start",
    "summary": "Prevent creating survey answers on start without pre-existing token",
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "license": "LGPL-3",
    "author": "Pierre Verkest, Odoo Community Association (OCA)",
    "maintainers": ["petrus-v"],
    "website": "https://github.com/OCA/survey",
    "depends": [
        "survey",
    ],
    "data": [
        "views/survey_survey_views.xml",
        "views/survey_templates.xml",
    ],
    "installable": True,
}
