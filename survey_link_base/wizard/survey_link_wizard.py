# Copyright 2024 Binhex - Adasat Torres de León
# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from werkzeug import urls

from odoo import _, api, fields, models


class SurveyLinkWizard(models.TransientModel):
    _name = "survey.link.wizard"
    _description = "Survey Link Wizard"

    survey_id = fields.Many2one(comodel_name="survey.survey", string="Survey")
    res_model = fields.Char()
    res_id = fields.Integer()
    partner_id = fields.Many2one("res.partner", string="Partner", readonly=True)
    date_deadline = fields.Date(
        string="Deadline to which the invitation to respond is valid",
        help="Deadline to which the invitation to\
        respond for this survey is valid. If the field is empty,\
        the invitation is still valid.",
    )
    share_link = fields.Char(readonly=True, store=True, compute="_compute_share_link")

    def _create_user_input_token(self):
        SurveyUserInput = self.env["survey.user_input"]

        survey_user_input = SurveyUserInput.search(
            [
                ("res_id", "=", self.res_id),
                ("res_model", "=", self.res_model),
                ("state", "in", ["new", "in_progress"]),
                ("partner_id", "=", self.partner_id.id),
                ("survey_id", "=", self.survey_id.id),
            ],
            limit=1,
        )

        if not survey_user_input:
            survey_user_input = self.survey_id._create_answer(
                email=self.partner_id.email,
                partner=self.partner_id,
                res_id=self.res_id,
                res_model=self.res_model,
            )
        return survey_user_input.access_token

    @api.depends("survey_id")
    def _compute_share_link(self):
        for record in self:
            if record.survey_id:
                user_input_token = record._create_user_input_token()
                record.share_link = urls.url_join(
                    record.survey_id.get_base_url(),
                    "/survey/%s/%s"
                    % (
                        record.survey_id.access_token,
                        user_input_token,
                    ),
                )
            else:
                record.share_link = False

    def action_start_survey(self):
        self.ensure_one()
        user_input_token = self._create_user_input_token()
        route = "/survey/" + self.survey_id.access_token + "/" + user_input_token
        return {
            "type": "ir.actions.act_url",
            "name": _("Survey"),
            "url": route,
            "target": "new",
        }
