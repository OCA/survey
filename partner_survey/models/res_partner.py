from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    survey_input_lines = fields.One2many(
        comodel_name="survey.user_input_line",
        inverse_name="partner_id",
        string="Surveys answers",
    )
    survey_inputs = fields.One2many(
        comodel_name="survey.user_input", inverse_name="partner_id", string="Surveys"
    )

    surveys_count = fields.Integer("Surveys Count", compute="_compute_surveys_count")
    surveys_company_count = fields.Integer(
        "Company Surveys Count", compute="_compute_surveys_company_count"
    )
    surveys_invisible = fields.Boolean(
        "Hide surveys link on partner contact if needed",
        compute="_compute_surveys_invisible",
    )
    surveys_company_invisible = fields.Boolean(
        "Hide surveys link on partner if needed",
        compute="_compute_surveys_company_invisible",
    )

    @api.depends("is_company")
    def _compute_surveys_count(self):
        read_group_res = (
            self.env["survey.user_input"]
            .sudo()
            .read_group([("partner_id", "in", self.ids)], ["partner_id"], "partner_id")
        )
        data = {res["partner_id"][0]: res["partner_id_count"] for res in read_group_res}
        for partner in self:
            partner.surveys_count = data.get(partner.id, 0)

    @api.depends("is_company", "child_ids.surveys_count")
    def _compute_surveys_company_count(self):
        self.surveys_company_count = sum(
            child.surveys_count for child in self.child_ids
        )

    @api.depends("is_company")
    def _compute_surveys_invisible(self):
        for partner in self:
            partner.surveys_invisible = (
                partner.surveys_count == partner.certifications_count
            )

    @api.depends("surveys_company_count", "certifications_company_count")
    def _compute_surveys_company_invisible(self):
        for partner in self:
            self.surveys_company_invisible = (
                partner.surveys_company_count == partner.certifications_company_count
            )

    def action_view_surveys(self):
        action = self.env.ref("partner_survey.res_partner_action_surveys").read()[0]
        action["view_mode"] = "tree"
        action["domain"] = [
            "|",
            ("partner_id", "in", self.ids),
            ("partner_id", "in", self.child_ids.ids),
        ]

        return action
