/** @odoo-module **/
/* Copyright 2026 Tecnativa - Eduardo Ezerouali
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import {_t} from "@web/core/l10n/translation";
import publicWidget from "@web/legacy/js/public/public_widget";
import SurveyFormWidget from "@survey/js/survey_form";

SurveyFormWidget.include({
    _prepareSubmitValues: function (formData, params) {
        this._super.apply(this, arguments);
        this.el.querySelectorAll('[data-question-type="model"]').forEach((el) => {
            const id = el.id?.replace("model_input_", "");
            const hiddenInput = this.el.querySelector("#model_value_" + id);
            if (hiddenInput && hiddenInput.name) {
                params[hiddenInput.name] = hiddenInput.value || "";
            }
        });
    },
});
publicWidget.registry.SurveyModelInput = publicWidget.Widget.extend({
    selector: ".o_survey_form",
    /**
     * @override
     */
    start: function () {
        const result = this._super.apply(this, arguments);
        this._choicesInstances = new Map();
        this._initAllInputs();
        this._setupObserver();
        return result;
    },
    /**
     * @override
     */
    destroy: function () {
        if (this._observer) {
            this._observer.disconnect();
            this._observer = null;
        }
        this._choicesInstances.forEach((instance) => instance.destroy());
        this._choicesInstances.clear();
        this._super.apply(this, arguments);
    },
    /**
     * @private
     */
    _initAllInputs: function () {
        const selects = document.querySelectorAll(".survey-model-select");
        selects.forEach((select) => {
            if (!select.dataset.choicesReady) {
                this._setupModelSelect(select);
            }
        });
    },
    /**
     * @private
     * @param {HTMLSelectElement} select
     */
    _setupModelSelect: function (select) {
        select.dataset.choicesReady = "true";
        const id = select.id.replace("model_input_", "");
        const hiddenValue = document.getElementById("model_value_" + id);
        const choicesInstance = new window.Choices(select, {
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
        this._choicesInstances.set(select, choicesInstance);
        select.addEventListener("change", function () {
            if (hiddenValue) {
                hiddenValue.value = select.value || "";
            }
        });
    },
    /**
     * @private
     */
    _setupObserver: function () {
        const self = this;
        const observer = new MutationObserver(function (mutations) {
            let needsInit = false;
            mutations.forEach(function (mutation) {
                mutation.addedNodes.forEach(function (node) {
                    if (node.nodeType !== 1) return;
                    if (node.classList?.contains("survey-model-select")) {
                        needsInit = true;
                    } else if (node.querySelector?.(".survey-model-select")) {
                        needsInit = true;
                    }
                });
            });
            if (needsInit) {
                requestAnimationFrame(() => self._initAllInputs());
            }
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true,
        });
    },
});

export default publicWidget.registry.SurveyModelInput;
