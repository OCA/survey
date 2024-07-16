odoo.define("survey_question_type_binary", [], function () {
    "use strict";

    const survey_form = odoo.loader.modules.get("@survey/js/survey_form")[
        Symbol.for("default")
    ];

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
            const binaryPrimises = self._getSubmitBinariesValues(params);

            if (binaryPrimises.length > 0 && !self.options.isStartScreen) {
                const $form = self.$("form");
                const formData = new FormData($form[0]);

                if (options.previousPageId) {
                    params.previous_page_id = options.previousPageId;
                }
                self._prepareSubmitValues(formData, params);
                var route = "/survey/submit";
                Promise.all(binaryPrimises).then(function () {
                    const submitPromise = self.rpc(
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
});
