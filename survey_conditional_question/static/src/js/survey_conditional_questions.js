odoo.define("survey.conditional_question", function(require) {
    "use strict";

    require("survey.survey");
    var the_form = $(".js_surveyform");

    function hide_conditional_questions() {
        // Hide the marked questions and pages
        var hidden_controller = the_form.attr("data-hidden");
        if (!_.isUndefined(hidden_controller)) {
            var hidden_def = $.ajax(hidden_controller, {dataType: "json"}).done(
                function(json_data) {
                    // For each of these, hide the question label and the answer
                    _.each(json_data.hidden_questions, function(key) {
                        the_form
                            .find(".js_question-wrapper[id=" + key + "]")
                            .css("display", "none");
                    });
                    _.each(json_data.hidden_pages, function(key) {
                        var div = the_form
                            .find(
                                "h1[data-oe-id=" +
                                    key +
                                    "][data-oe-model='survey.page']"
                            )
                            .parent();
                        div.css("display", "none");
                        // Also hide the adjacent hr tag
                        div.prev().css("display", "none");
                    });
                }
            );
        }
    }

    if (the_form.length) {
        hide_conditional_questions();
    }
});
