/** @odoo-module **/
/* global FileReader, FormData */
import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

publicWidget.registry.SurveyFormWidget.include({
    _getSubmitBinaryValues(params) {
        const self = this;
        let promises = [];
        for (const el of self.el.querySelectorAll("[data-question-type]")) {
            switch (el.dataset.questionType) {
                case "binary":
                case "multi_binary":
                    promises = promises.concat(
                        self._getSubmitAnswersBinary(params, el)
                    );
                    break;
            }
        }
        return promises;
    },
    _getSubmitAnswersBinary(params, el) {
        const question_id = el.name;
        return Array.prototype.map.call(el.files, (file) => {
            return this._readFileAsDataURL(file).then(function (sDataURL) {
                if (!params[question_id]) {
                    params[question_id] = [];
                }
                params[question_id].push({
                    data: sDataURL.split(",")[1],
                    filename: file.name,
                    size: file.size,
                    type: file.type,
                });
            });
        });
    },
    _readFileAsDataURL(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    },
    _submitForm: async function (options) {
        const self = this;
        const params = {};
        const binaryPromises = self._getSubmitBinaryValues(params);
        if (binaryPromises.length > 0 && !self.options.isStartScreen) {
            const $form = self.$("form");
            const formData = new FormData($form[0]);
            if (options.previousPageId) {
                params.previous_page_id = options.previousPageId;
            }
            self._prepareSubmitValues(formData, params);
            const route = "/survey/submit";
            Promise.all(binaryPromises).then(function () {
                const submitPromise = rpc(
                    `${route}/${self.options.surveyToken}/${self.options.answerToken}`,
                    params
                );
                self._nextScreen(submitPromise, options);
            });
        } else {
            return self._super(options);
        }
    },
});
