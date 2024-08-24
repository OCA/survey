# Copyright 2016 Tecnativa, S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Remove Odoo Branding from Survey",
    "version": "16.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "license": "AGPL-3",
    "category": "Marketing/Surveys",
    "depends": ["survey"],
    "data": ["templates/disable_odoo.xml"],
    "installable": True,
    "post_init_hook": "post_init_hook",
}
