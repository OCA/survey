# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty
# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models


class CRMLead(models.Model):
    _name = "crm.lead"
    _inherit = ["crm.lead", "survey.link.mixin"]

    def get_default_survey(self):
        res = super().get_default_survey()
        if self.env.company.survey_crm_id:
            return self.env.company.survey_crm_id.id
        return res
