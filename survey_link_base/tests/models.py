# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class TestSurveyMixinModel(models.Model):
    _name = "test.survey.mixin"
    _inherit = "survey.link.mixin"
    _auto = True

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    name = fields.Char(string="Test Field")

    def get_default_survey(self):
        return self.env.context.get("default_survey_id", False)
