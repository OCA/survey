/** @odoo-module **/
/* Copyright 2022 Tecnativa - David Vidal
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import SurveyFormWidget from "@survey/js/survey_form";
import {_t} from "@web/core/l10n/translation";

SurveyFormWidget.include({
    /**
     * Validate legal terms acceptance if present
     *
     * @override
     * * @param {JQuery} [$form] the survey form
     * @returns {Boolean}
     */
    _validateForm: function ($form) {
        const [$legalTermsInput] = $form.find("#accepted_legal_terms");
        const res = this._super(...arguments);
        // The original method returns false when there are errors. We can break here
        if (!res || !$legalTermsInput) {
            return res;
        }
        if (!$legalTermsInput.checked) {
            this._showErrors({
                accepted_legal_terms_wrapper: _t("You must accept the legal terms"),
            });
            return false;
        }
        return res;
    },
});
