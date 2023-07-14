/* Copyright 2023 Aures Tic - Jose Zambudio
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("survey_question_type_binary", function (require) {
    "use strict";

    const survey_form = require("survey.form");

    survey_form.include({
        _getSubmitBinariesValues: function (params) {
            const self = this;
            let promises = [];

            this.$("[data-question-type]").each(function () {
                switch ($(this).data("questionType")) {
                    case "binary":
                    case "multi_binary":
                        promises = promises.concat(
                            self._getSubmitAnswersBinary(params, $(this))
                        );
                        break;
                }
            });
            return promises;
        },
        _getSubmitAnswersBinary: function (params, $input) {
            const question_id = $input.attr("name");
            return Array.prototype.map.call($input[0].files, (file) => {
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
        _readFileAsDataURL: function (file) {
            return $.Deferred(function (deferred) {
                $.extend(new FileReader(), {
                    onload: function (e) {
                        var sDataURL = e.target.result;
                        deferred.resolve(sDataURL);
                    },
                    onerror: function () {
                        deferred.reject(this);
                    },
                }).readAsDataURL(file);
            }).promise();
        },
        _submitForm: function (options) {
            const self = this;
            const params = {};
            const binaryPrimises = this._getSubmitBinariesValues(params);
            if (binaryPrimises.length > 0 && !this.options.isStartScreen) {
                const $form = this.$("form");
                const formData = new FormData($form[0]);

                if (options.previousPageId) {
                    params.previous_page_id = options.previousPageId;
                }
                this._prepareSubmitValues(formData, params);
                Promise.all(binaryPrimises).then(function () {
                    const submitPromise = self._rpc({
                        route: _.str.sprintf(
                            "%s/%s/%s",
                            "/survey/submit",
                            self.options.surveyToken,
                            self.options.answerToken
                        ),
                        params: params,
                    });
                    self._nextScreen(submitPromise, options);
                });
            } else {
                return this._super(options);
            }
        },
    });
});
