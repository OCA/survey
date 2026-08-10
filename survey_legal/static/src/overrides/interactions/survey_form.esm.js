/* Copyright 2022 Tecnativa - David Vidal
   Copyright 2026 Tecnativa - Adasat Torres de León
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import {_t} from "@web/core/l10n/translation";
import {patch} from "@web/core/utils/patch";
import {SurveyForm} from "@survey/interactions/survey_form";

patch(SurveyForm.prototype, {
    validateForm(formEl, formData) {
        const res = super.validateForm(formEl, formData);
        const $legalTermsInput = formEl.querySelector("#accepted_legal_terms");
        if ($legalTermsInput && !$legalTermsInput.checked) {
            this.showErrors({
                accepted_legal_terms_wrapper: _t("You must accept the legal terms"),
            });
            return false;
        }
        return res;
    },
});
