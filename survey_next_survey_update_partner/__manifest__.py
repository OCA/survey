# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Update generated partner on next survey",
    "summary": "Update the partner values when it's generated from the previous survey",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing/Survey",
    "website": "https://github.com/OCA/survey",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["survey_contact_generation", "survey_answer_generation"],
    "data": [],
    "demo": ["demo/survey_update_generated_partner_demo.xml"],
    "assets": {
        "web.assets_tests": ["survey_next_survey_update_partner/static/tests/*.js"],
    },
}
