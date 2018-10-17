/* Copyright 2018 ACSONE SA/NV
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).*/
odoo.define('survey_question_type_five_star.survey', function(require) {
    'use strict';
    $(document).ready(function() {
        //Print Result case
        var the_form = $('.js_surveyform');
        var prefill_controller = the_form.attr("data-prefill");
        if (!the_form.length) {
            return $.Deferred().reject("DOM doesn't contain '.js_surveyform'");
        }
        function prefill() {
            if (!_.isUndefined(prefill_controller)) {
                var prefill_def = $.ajax(prefill_controller, {
                        dataType: "json"
                    })
                    .done(function(json_data) {
                        _.each(json_data, function(value, key) {
                            var input = the_form.find(".form-control[name=" + key + "]");
                            $(input).parent().find("label").each(function(label_index) {
                                if ((5 - label_index) <= value) {
                                    $(this).addClass("checked");
                                }
                            });
                        });
                    })
                    .fail(function() {
                        console.warn("[survey Question Type Five Star] Unable to load prefill data");
                    });
                return prefill_def;
            }
        }
        prefill();
        // Answer Case
        $(".rate > label").click(function() {
            var label_items = $(this).parent().find("label");
            var value = label_items.length - $(this).index();
            label_items.removeClass("checked");
            label_items.slice($(this).index()).addClass("checked");
            $(this).parent().find("input").val(value);
        });
    });

});