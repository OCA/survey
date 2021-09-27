odoo.define("survey.conditional_question", function () {
    "use strict";

    var the_form = $(".js_surveyform");
    if (!the_form.length) {
        return $.Deferred();
    }
    function hide_conditional_questions() {
        // Hide the marked questions and pages
        var hidden_controller = the_form.attr("data-hidden");
        if (!_.isUndefined(hidden_controller)) {
            $.ajax(hidden_controller, {dataType: "json"}).done(function (json_data) {
                // For each of these, hide the question label and the answer
                _.each(json_data.hidden_questions, function (key) {
                    the_form
                        .find(".js_question-wrapper[id=" + key + "]")
                        .addClass("hidden");
                });
                _.each(json_data.hidden_pages, function (key) {
                    var div = the_form
                        .find("h1[data-oe-id=" + key + "][data-oe-model='survey.page']")
                        .parent();
                    div.addClass("hidden");
                    // Also hide the adjacent hr tag
                    div.prev().addClass("hidden");
                });
            });
        }
    }

    function _survey_conditional_on_change(event) {
        // Hide or show conditional questions on the same page
        var target = event.target;
        var value = target.value;
        if (value === -1) {
            return;
        }
        var type = target.getAttribute("type");
        var question = target.name.split("_")[1];
        if ($(target).is("select") || type === "radio") {
            the_form
                .find('[triggering_question_id="' + question + '"]')
                .each(function (index, item) {
                    if (item.getAttribute("triggering_answer_id") === value) {
                        $(item).removeClass("hidden");
                    } else {
                        $(item).addClass("hidden");
                    }
                });
        } else if (type === "checkbox") {
            the_form
                .find('[triggering_question_id="' + question + '"]')
                .each(function (index, item) {
                    if (item.getAttribute("triggering_answer_id") === value) {
                        if (target.checked) {
                            $(item).removeClass("hidden");
                        } else {
                            $(item).addClass("hidden");
                        }
                    }
                });
        } else {
            // In this case, we are managing a number
            the_form
                .find('[triggering_question_id="' + question + '"]')
                .each(function (index, item) {
                    var min_value = parseFloat(
                        item.getAttribute("triggering_question_min")
                    );
                    var max_value = parseFloat(
                        item.getAttribute("triggering_question_max")
                    );
                    var float_value = parseFloat(value);
                    if (min_value <= float_value && max_value >= float_value) {
                        $(item).removeClass("hidden");
                    } else {
                        $(item).addClass("hidden");
                    }
                });
        }
    }
    // Hide conditional questions depending on questions on earlier pages
    hide_conditional_questions();
    // Set onchange events on all simple and multiple choice answers
    if (the_form.is("form")) {
        the_form.find("label > input[type='checkbox']").each(function (index, item) {
            $(item).change(_survey_conditional_on_change);
            _survey_conditional_on_change({target: item});
        });
        the_form.find("label > input[type='radio']").each(function (index, item) {
            $(item).change(_survey_conditional_on_change);
            _survey_conditional_on_change({target: item});
        });
        the_form.find("select").each(function (index, item) {
            $(item).change(_survey_conditional_on_change);
            _survey_conditional_on_change({target: item});
        });
        the_form.find("input[type='number']").each(function (index, item) {
            console.log(item.value);
            $(item).change(_survey_conditional_on_change);
            _survey_conditional_on_change({target: item});
        });
    }
});
