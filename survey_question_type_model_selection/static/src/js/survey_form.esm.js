/* Copyright 2026 Tecnativa - Eduardo Ezerouali
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import {_t} from "@web/core/l10n/translation";
import {patch} from "@web/core/utils/patch";
import {registry} from "@web/core/registry";
import {Interaction} from "@web/public/interaction";
import {SurveyForm} from "@survey/interactions/survey_form";

patch(SurveyForm.prototype, {
    prepareSubmitValues(formData, params) {
        super.prepareSubmitValues(...arguments);
        this.el.querySelectorAll('[data-question-type="model"]').forEach((el) => {
            const id = el.id?.replace("model_input_", "");
            const hiddenInput = this.el.querySelector("#model_value_" + id);
            if (hiddenInput && hiddenInput.name) {
                params[hiddenInput.name] = hiddenInput.value || "";
            }
        });
    },
});

export class SurveyModelInput extends Interaction {
    static selector = ".survey-model-select";
    setup() {
        this.choicesInstance = null;
    }

    /**
     * @override
     */
    start() {
        const id = this.el.id.replace("model_input_", "");
        this.hiddenValue = this.el.ownerDocument.getElementById("model_value_" + id);
        this.choicesInstance = new window.Choices(this.el, {
            searchEnabled: true,
            searchPlaceholderValue: _t("Type to search..."),
            itemSelectText: "",
            shouldSort: false,
            allowHTML: false,
            removeItemButton: false,
            placeholder: true,
            placeholderValue: _t("Select or type..."),
            noResultsText: _t("No results found"),
            noChoicesText: _t("No options available"),
        });
        this.addListener(this.el, "change", () => {
            if (this.hiddenValue) {
                this.hiddenValue.value = this.el.value || "";
            }
        });
    }

    /**
     * @override
     */
    destroy() {
        this.choicesInstance?.destroy();
        this.choicesInstance = null;
    }
}

registry
    .category("public.interactions")
    .add("survey_question_type_model_selection.SurveyModelInput", SurveyModelInput);
