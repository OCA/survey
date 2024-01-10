from odoo import models


class ResPartner(models.Model):
    _inherit = ["res.partner", "survey.representative.mixin"]
    _name = "res.partner"
