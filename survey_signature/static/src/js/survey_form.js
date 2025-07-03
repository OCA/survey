odoo.define("survey_signature.form", function (require) {
    "use strict";

    var SurveyForm = require("survey.form");

    SurveyForm.include({
        start: function () {
            this._super.apply(this, arguments);
            this._initSign();
        },

        _onNextScreenDone: function () {
            var self = this;
            this._super.apply(this, arguments);
            self._initSign();
        },

        _initSign: function () {
            $(document).ready(function () {
                $(this)
                    .find(".o_signature_container")
                    .each(function () {
                        var self = this;

                        $(this).find(".signature").jSignature();

                        $(this).find(".signature").data("empty", true);

                        $(this)
                            .find(".signature")
                            .on("change", function () {
                                var data = $(this).jSignature("getData", "image");
                                $(this).data("value", data[1]);

                                if ($(this).data("value")) {
                                    $(this).data("empty", false);
                                }
                            });

                        $(this)
                            .find(".clear_sign")
                            .on("click", function () {
                                $(self).find(".signature").jSignature("reset");
                                $(self).find(".signature").data("empty", true);
                            });
                    });
            });
        },

        _validateForm: function ($form, formData) {
            var errors = {};
            this._resetErrors();
            var data = {};
            formData.forEach(function (value, key) {
                data[key] = value;
            });

            var inactiveQuestionIds = this.options.sessionInProgress
                ? []
                : this._getInactiveConditionalQuestionIds();

            $form.find("[data-question-type]").each(function () {
                var $input = $(this);
                var $questionWrapper = $input.closest(".js_question-wrapper");
                var questionId = $questionWrapper.attr("id");
                if (inactiveQuestionIds.includes(parseInt(questionId))) {
                    return;
                }
                var questionRequired = $questionWrapper.data("required");
                var constrErrorMsg = $questionWrapper.data("constrErrorMsg");
                switch ($input.data("questionType")) {
                    case "signature":
                        if (questionRequired) {
                            if ($questionWrapper.find(".signature").data("empty")) {
                                errors[questionId] = constrErrorMsg;
                            }
                        }
                        break;
                }
            });
            if (_.keys(errors).length > 0) {
                this._showErrors(errors);
                return false;
            }
            return this._super.apply(this, arguments);
        },

        _prepareSubmitValues: function (formData, params) {
            this._super.apply(this, arguments);
            var self = this;
            formData.forEach(function (value, key) {
                switch (key) {
                    case "csrf_token":
                    case "token":
                    case "page_id":
                    case "question_id":
                        params[key] = value;
                        break;
                }
            });

            // Get all question answers by question type
            this.$("[data-question-type]").each(function () {
                switch ($(this).data("questionType")) {
                    case "signature":
                        params = self._prepareSubmitSignature(params, $(this));
                        break;
                }
            });
        },

        _prepareSubmitSignature: function (params, dom) {
            var questionId = dom.data("name");
            params[questionId] = dom.find(".signature").data("value");
            return params;
        },
    });

    return SurveyForm;
});
