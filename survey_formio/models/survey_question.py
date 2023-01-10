# Copyright 2023 Acsone SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models

ODOO_TO_FORM_IO_TYPES_DICT = {
    "free_text": "textarea",
    "textbox": "textfield",
    "numerical_box": "number",
    "date": "datetime",
    "datetime": "datetime",
    "simple_choice": "radio",
    "multiple_choice": "selectboxes",
}


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    def _get_formio_common_parameters(self):
        """
        Returns a dict representing the common parameters for all form.io components.

        Form.io parameters:
        - type : required
        - key : required
        - input : required but no corresponding parameter in survey.
                  Set to default form.io value
        - label
        - validate : only constr_mandatory supported at the moment,
                     will be handled in its own function

        See https://github.com/formio/formio.js/wiki/Components-JSON-Schema#common-parameters
        for more information
        """
        self.ensure_one()
        return {
            "type": ODOO_TO_FORM_IO_TYPES_DICT[self.question_type],
            "key": f"q{self.id}",
            "input": True,
            "label": self.title,
        }

    def _get_formio_validate_parameters(self):
        """
        Returns a dict representing the validation parameters of a form.io component

        Form.io parameters:
        - validate.required
        """
        self.ensure_one()
        return {"validate": {"required": self.constr_mandatory}}

    def _get_formio_textarea_parameters(self):
        """
        Returns a dict containing parameters specific to a text area component

        Form.io parameters:
        - rows : required but no corresponding parameter in survey.
                 Set to default form.io value
        """
        self.ensure_one()
        return {
            "rows": 3,
        }

    def _get_formio_textfield_parameters(self):
        """
        Returns a dict containing parameters specific to a text field component

        This function does not take validation_length_min, validation_length_max
        and validation_error_msg into account yet.
        """
        self.ensure_one()
        return {}

    def _get_formio_number_parameters(self):
        """
        Returns a dict containing parameters specific to a number component

        This function does not take validation_min_float_value and validation_max_float_value
        into account yet.

        Form.io parameters:
        - validate.min : not supported at the moment
        - validate.max : not supported at the moment
        """
        self.ensure_one()
        return {}

    def _get_formio_datetime_parameters(self, is_datetime=True):
        """
        Returns a dict containing parameters specific to a datetime component

        This function does not take validation_min_date_time, validation_max_date_time
        and validation_error_msg into account yet.

        Parameters:
        is_datetime: boolean that determines if the time picker is available or not

        Form.io parameters:
        - datePicker.minMode : required but no corresponding parameter in survey.
                               Set to default form.io value
        - datePicker.maxMode : required but no corresponding parameter in survey.
                               Set to default form.io value
        - timePicker.hourStep : required but no corresponding parameter in survey.
                                Set to default form.io value
        - timePicker.minuteStep : required but no corresponding parameter in survey.
                                  Set to default form.io value
        """
        self.ensure_one()
        return {
            "datepicker": {"minMode": "day", "maxMode": "year"},
            "timePicker": {"hourStep": 1, "minuteStep": 1},
            "enableTime": is_datetime,
        }

    def _get_formio_radio_parameters(self):
        """
        Returns a dict containing parameters specific to a radio component

        This function does not take display_mode, column_nb and comments_allowed
        into account yet.

        Form.io parameters:
        - values: list of dict {"label": label, "value": value}
        """
        self.ensure_one()
        return {
            "values": [
                {"label": label.value, "value": f"a{label.id}"}
                for label in self.labels_ids
            ]
        }

    def _get_formio_selectboxes_parameters(self):
        """
        Returns a dict containing parameters specific to a select boxes component

        This function does not take column_nb and comments_allowed into account yet.

        Form.io parameters:
        - values: list of dict {"label": label, "value": value}
        """
        self.ensure_one()
        return {
            "values": [
                {"label": label.value, "value": f"a{label.id}"}
                for label in self.labels_ids
            ]
        }

    def _get_formio_component(self):
        """
        Returns a dict representing a question as a valid formio component
        """
        self.ensure_one()

        specific = {}
        if self.question_type == "free_text":
            specific = self._get_formio_textarea_parameters()
        elif self.question_type == "textbox":
            specific = self._get_formio_textfield_parameters()
        elif self.question_type == "numerical_box":
            specific = self._get_formio_number_parameters()
        elif self.question_type == "date":
            specific = self._get_formio_datetime_parameters(is_datetime=False)
        elif self.question_type == "datetime":
            specific = self._get_formio_datetime_parameters()
        elif self.question_type == "simple_choice":
            specific = self._get_formio_radio_parameters()
        elif self.question_type == "multiple_choice":
            specific = self._get_formio_selectboxes_parameters()
        else:
            # This question_type is not supported
            return False

        common = self._get_formio_common_parameters()
        validate = self._get_formio_validate_parameters()
        # merge validate and specific dictionnaries
        if specific.get("validate"):
            specific["validate"].update(validate["validate"])
        else:
            specific.update(validate)
        common.update(specific)
        return common
