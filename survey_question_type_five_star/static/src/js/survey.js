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
            label_items.removeClass("checked fa-star");
            label_items.addClass("fa-star-o");
            label_items.slice($(target).index()).addClass("checked fa-star");
            label_items.slice($(target).index()).removeClass("fa-star-o");
            $(target).parent().find("input").val(value);
            $(target).parent().find("input").trigger("change");
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
    });
});
