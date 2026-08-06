from odoo import models


class ResPartner(models.Model):
    _inherit = ["survey.representative.mixin"]
    _name = "test.model"
    _description = "test model description"
