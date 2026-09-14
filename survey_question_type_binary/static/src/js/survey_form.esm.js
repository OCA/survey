import {SurveyForm} from "@survey/interactions/survey_form";
import {rpc} from "@web/core/network/rpc";
import {patch} from "@web/core/utils/patch";

patch(SurveyForm.prototype, {
    getSubmitBinaryValues(params) {
        const self = this;
        let promises = [];
        for (const el of self.el.querySelectorAll("[data-question-type]")) {
            switch (el.dataset.questionType) {
                case "binary":
                case "multi_binary":
                    promises = promises.concat(self.getSubmitAnswersBinary(params, el));
                    break;
            }
        }
        return promises;
    },
    getSubmitAnswersBinary(params, el) {
        const question_id = el.name;
        return Array.prototype.map.call(el.files, (file) => {
            return this.readFileAsDataURL(file).then(function (sDataURL) {
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
    readFileAsDataURL(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    },
    async submitForm(options = {}) {
        const self = this;
        const params = {};
        const binaryPromises = self.getSubmitBinaryValues(params);
        if (binaryPromises.length > 0 && !self.options.isStartScreen) {
            const formData = new FormData(self.formEl);
            if (options.previousPageId) {
                params.previous_page_id = options.previousPageId;
            }
            this.prepareSubmitValues(formData, params);
            const route = "/survey/submit";
            Promise.all(binaryPromises).then(function () {
                const submitPromise = rpc(
                    `${route}/${self.options.surveyToken}/${self.options.answerToken}`,
                    params
                );
                self.nextScreen(submitPromise, options);
            });
        } else {
            return super.submitForm(options);
        }
    },
});
