/* Copyright 2018 ACSONE SA/NV
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).*/
odoo.define("survey_question_type_five_star.survey", function() {
    "use strict";
    $(document).ready(function() {
        // Print Result case
        var the_form = $(".js_surveyform");
        var prefill_controller = the_form.attr("data-prefill");
        if (!the_form.length) {
            return $.Deferred();
        }

        function prefill() {
            if (!_.isUndefined(prefill_controller)) {
                var prefill_def = $.ajax(prefill_controller, {
                    dataType: "json",
                })
                    .done(function(json_data) {
                        _.each(json_data, function(value, key) {
                            var input = the_form.find(
                                ".form-control[name=" + key + "]"
                            );
                            if (
                                !$(input)
                                    .parent()
                                    .hasClass("print_star_rate")
                            ) {
                                return;
                            }
                            $(input)
                                .parent()
                                .find("label")
                                .each(function(label_index) {
                                    if (5 - label_index <= value) {
                                        $(this).addClass("checked fa-star");
                                        $(this).removeClass("fa-star-o");
                                    }
                                });
                        });
                    })
                    .fail(function() {
                        console.warn("[survey Question Five Star] Unable to prefill");
                    });
                return prefill_def;
            }
        }
        prefill();
        // Answer Case
        $(".rate > label").click(function() {
            var label_items = $(this)
                .parent()
                .find("label");
            var value = label_items.length - $(this).index();
            label_items.removeClass("checked fa-star");
            label_items.addClass("fa-star-o");
            label_items.slice($(this).index()).addClass("checked fa-star");
            label_items.slice($(this).index()).removeClass("fa-star-o");
            $(this)
                .parent()
                .find("input")
                .val(value);
        });
    });
});
