/* Copyright 2018 ACSONE SA/NV
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).*/
odoo.define("survey_question_type_five_star.survey", function (require) {
    "use strict";
    var SurveyFormWidget = require("survey.form");
    SurveyFormWidget.include({
        events: _.extend({}, SurveyFormWidget.prototype.events, {
            "click .rate > label": "_onClickFiveStarLabel",
        }),
        _onClickFiveStarLabel: function (event) {
            if (this.readonly) {
                return;
            }
            var target = event.target;
            var label_items = $(target).parent().find("label");

            var value = label_items.length - $(target).index();
            label_items.removeClass("checked fa-star").addClass("fa-star-o");
            label_items
                .slice($(target).index())
                .addClass("checked fa-star")
                .removeClass("fa-star-o");
            var $input = $(target).parent().find("input");
            $input.val(value);
            $input.trigger("change");
        },
        _prepareSubmitValues: function (formData, params) {
            this._super.apply(this, arguments);
            this.$("[data-question-type]").each(function () {
                switch ($(this).data("questionType")) {
                    case "star_rate":
                        params[this.name] = this.value;
                        break;
                }
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

                // If question is inactive, skip validation.
                if (inactiveQuestionIds.includes(parseInt(questionId))) {
                    return;
                }

                var questionRequired = $questionWrapper.data("required");
                var constrErrorMsg = $questionWrapper.data("constrErrorMsg");
                var validationErrorMsg = $questionWrapper.data("validationErrorMsg");

                switch ($input.data("questionType")) {
                    case "star_rate":
                        if (questionRequired && !$input.val()) {
                            errors[questionId] = constrErrorMsg || validationErrorMsg;
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
    });
});
