# Copyright 2025 Kencove - Mohamed Alkobrosli
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import OrderedDict

from odoo import http
from odoo.http import request
from odoo.tools import format_date, format_datetime, is_html_empty

from odoo.addons.survey.controllers.main import Survey


class CustomSurvey(Survey):
    def render_value(self, value):
        if value:
            partner = request.env.user.partner_id
            render_env = request.env["mail.render.mixin"].sudo()
            try:
                rendered_answer = render_env._render_template(
                    value, partner._name, [partner.id]
                )[partner.id]
                return rendered_answer or False
            except Exception as e:
                # handel ValueError raised for NameError or AttributeError
                error_msg = str(e).lower()
                if "nameerror" in error_msg or "attributeerror" in error_msg:
                    return False
                else:
                    raise
        return False

    def get_prefilled_answers(self, questions):
        # require participants to be logged in to make sure thier own field values be filled in
        # and not the public user field values
        prefilled_answers = OrderedDict()
        for question in questions or []:
            if question.question_type in (
                "simple_choice",
                "multiple_choice",
            ):
                suggested_answer_ids = question.suggested_answer_ids
                for suggested_answer_id in suggested_answer_ids:
                    suggested_answer_value = suggested_answer_id.value
                    rendered_answer = self.render_value(suggested_answer_value)
                    if rendered_answer:
                        prefilled_answers[suggested_answer_id] = rendered_answer
            elif question.question_type == "char_box":
                suggested_answer_value = question.suggested_prefilled_answer
                rendered_answer = self.render_value(suggested_answer_value)
                if rendered_answer:
                    prefilled_answers[question] = rendered_answer
            elif question.question_type == "text_box":
                suggested_answer_value = question.suggested_prefilled_answer_multi
                rendered_answer = self.render_value(suggested_answer_value)
                if rendered_answer:
                    prefilled_answers[question] = rendered_answer
        return prefilled_answers

    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        data = super()._prepare_survey_data(survey_sudo, answer_sudo, **post)
        if survey_sudo.users_login_required:
            questions = survey_sudo.question_ids
            data["prefilled_answers"] = self.get_prefilled_answers(questions)
        return data

    @http.route(
        "/survey/print/<string:survey_token>",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def survey_print(self, survey_token, review=False, answer_token=None, **post):
        """Display an survey in printable view; if <answer_token> is set, it will
        grab the answers of the user_input_id that has <answer_token>."""
        access_data = self._get_access_data(
            survey_token, answer_token, ensure_token=False, check_partner=False
        )
        if access_data["validity_code"] is not True and (
            access_data["has_survey_access"]
            or access_data["validity_code"]
            not in ["token_required", "survey_closed", "survey_void", "answer_deadline"]
        ):
            return self._redirect_with_error(access_data, access_data["validity_code"])
        survey_sudo, answer_sudo = (
            access_data["survey_sudo"],
            access_data["answer_sudo"],
        )
        questions = answer_sudo._get_print_questions()
        prefilled_answers = self.get_prefilled_answers(questions)
        return request.render(
            "survey.survey_page_print",
            {
                "is_html_empty": is_html_empty,
                "review": review,
                "survey": survey_sudo,
                "answer": answer_sudo
                if survey_sudo.scoring_type != "scoring_without_answers"
                else answer_sudo.browse(),
                "questions_to_display": answer_sudo._get_print_questions(),
                "scoring_display_correction": survey_sudo.scoring_type
                == "scoring_with_answers"
                and answer_sudo,
                "format_datetime": lambda dt: format_datetime(
                    request.env, dt, dt_format=False
                ),
                "format_date": lambda date: format_date(request.env, date),
                "prefilled_answers": prefilled_answers,
            },
        )
