# Copyright 2025 Kencove - Mohamed Alkobrosli (http://kencove.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Partner Survey SMS",
    "summary": "Send survey participation link via SMS",
    "category": "Marketing/Surveys",
    "version": "18.0.1.0.0",
    "author": "Kencove, Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "license": "AGPL-3",
    "depends": [
        "survey",
        "sms",
        "html_text",
    ],
    "data": [
        "data/sms_template.xml",
        "wizard/survey_invite_views.xml",
    ],
    "installable": True,
}
