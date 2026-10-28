# Copyright 2026 Acsone
# @author Pierre Verkest <pierre.verkest@apycod.fr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import fields, models


class Survey(models.Model):
    _inherit = "survey.survey"

    prevent_create_on_start = fields.Boolean(
        string="Prevent creating answers on start",
        help="If checked, respondents cannot create a new answer directly "
        "from the survey start link without a pre-existing answer token.",
    )
