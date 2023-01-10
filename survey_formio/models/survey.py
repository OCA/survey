# Copyright 2023 Acsone SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from datetime import datetime

import pytz

from odoo import models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    def _get_formio_display(self):
        """
        Returns a string representing the form.io display
        Correct values are form, wizard or pdf. At the moment only
        form is supported.
        In the future use questions_layout to determine display.
        """
        self.ensure_one()
        return "form"

    def _get_survey_title(self):
        """
        Returns a dict representing the title of the survey as a form.io
        component.
        """
        self.ensure_one()
        return {
            "label": "title",
            "tag": "h1",
            "content": self.title,
            "key": "title",
            "type": "htmlelement",
        }

    def _get_formio_components(self):
        """
        Pages are not supported yet.

        Returns a list of dict representing survey questions as form.io components
        """
        self.ensure_one()
        components = []
        components.append(self._get_survey_title())
        for question in self.question_ids:
            component = question._get_formio_component()
            if component:
                components.append(component)
        return components

    def _from_formio_datetime_to_odoo(self, datetime_str):
        """
        Form.io datetimes are given in the user's timezone and with an offset.
        Odoo wants naïve datetimes.

        Returns a naïve datetime as a string

        Parameters:
        datetime_str: string representing a datetime with an offset
        """
        # In the json given by form.io, the offset is formatted as +hh:mm
        # To be able to use strptime we need it to be formated as +hhmm

        # We can't use the fromisoformat function because it's only available
        # in Python v3.7+ and Odoo v13 is compatible with Python v3.6
        index = datetime_str.rfind(":")
        datetime_str = datetime_str[:index] + datetime_str[index + 1 :]
        utc_datetime = datetime.strptime(
            datetime_str, "%Y-%m-%dT%H:%M:%S%z"
        ).astimezone(pytz.UTC)
        return utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

    def _from_formio_multiple_choice_to_odoo(
        self, question_id, multiple_choice_answers_dict
    ):
        """
        For a multiple choice question, the form.io answer has the
        following format:
        {"question_id": {
          "answer_1_value": true/false
          "answer_2_value": true/false
          ....
        }}
        Odoo expects the following format:
        {"question_id_answer_id": "answer_id"}

        Returns a dictionnary with the correct format.

        Parameters:
        question_id: id of the survey.question
        multiple_choice_answers_dict: dict given by form.io for a multiple choice question
        """
        answers_dict = {}
        for answer in multiple_choice_answers_dict.keys():
            answers_dict[question_id + "_" + answer[1:]] = answer[1:]
        return answers_dict

    def generate_formio_json(self):
        """
        Returns a form.io conform json representation of a survey.
        """
        self.ensure_one()
        display = self._get_formio_display()
        title = self.title
        components = self._get_formio_components()

        form_json = json.dumps(
            {"display": display, "title": title, "components": components}
        )
        return form_json

    def user_input_from_formio(self, formio_output, user_input_id=None):
        """
        If no user_input_id is given, creates a user_input with the values in formio_output.
        If there is a user_input_id, updates that user_input with the values in formio_output.

        Parameters:
        formio_output: json given by form.io as a dictionnary
        user_input_id: survey.user_input id
        """
        if not user_input_id:
            user_input_id = self.env["survey.user_input"].create({"survey_id": self.id})
        else:
            user_input_id = self.env["survey.user_input"].browse(user_input_id)
        form_io_answers = formio_output["data"]
        for question in self.question_ids:
            question_label = f"q{question.id}"
            if form_io_answers.get(question_label):
                if question.question_type == "datetime":
                    form_io_answers[
                        question_label
                    ] = self._from_formio_datetime_to_odoo(
                        form_io_answers[question_label]
                    )
                if question.question_type == "date":
                    # We only need the date part of the string, not the hours
                    form_io_answers[question_label] = form_io_answers[question_label][
                        :10
                    ]
                if question.question_type == "numerical_box":
                    # Odoo expects a string but form.io gives a number
                    # we have to cast it to avoid an error
                    form_io_answers[question_label] = str(
                        form_io_answers[question_label]
                    )
                if question.question_type == "simple_choice":
                    # Odoo expects a string but form.io gives a number
                    # we have to cast it to avoid an error
                    form_io_answers[question_label] = form_io_answers[question_label][
                        1:
                    ]
                if question.question_type == "multiple_choice":
                    answers_dict = form_io_answers[question_label]
                    form_io_answers.pop(question_label)
                    form_io_answers.update(
                        self._from_formio_multiple_choice_to_odoo(
                            question_label, answers_dict
                        )
                    )
                self.env["survey.user_input_line"].save_lines(
                    user_input_id.id, question, form_io_answers, question_label
                )
        return user_input_id
