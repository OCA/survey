odoo.define("survey.conditional_question", function (require) {
    "use strict";

    var SurveyFormWidget = require("survey.form");
    SurveyFormWidget.include({
        events: _.extend({}, SurveyFormWidget.prototype.events, {
            "change input[type='number']": "_onChangeInputNumber",
        }),
        _onChangeInputNumber: function (event) {
            if (this.options.questionsLayout !== "page_per_question") {
                var $target = $(event.currentTarget);
                var questionId = $target[0].name;
                var result = parseFloat($target[0].value);
                if (this.options.noAnswerConditionalQuestionsByQuestion[questionId]) {
                    _.forEach(
                        this.options.noAnswerConditionalQuestionsByQuestion[questionId],
                        function (question_data) {
                            var dependingQuestion = $(
                                ".js_question-wrapper#" + question_data[0]
                            );
                            if (
                                result < question_data[1] ||
                                question_data[2] < result
                            ) {
                                dependingQuestion.addClass("d-none");
                            } else {
                                dependingQuestion.removeClass("d-none");
                            }
                        }
                    );
                }
            }
        },
    });
});
