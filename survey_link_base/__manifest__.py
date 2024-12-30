# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Survey Link Base",
    "summary": """
        This addon creates a mixin and a wizard to enable the
        generation of surveys from other models.""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Binhex, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "depends": ["survey", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/survey_link_wizard_views.xml",
    ],
    "external_dependencies": {
        "python": ["odoo-test-helper"],
    },
}
