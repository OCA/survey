odoo.define("survey.date_filter", function() {
    "use strict";

    if (!$(".js_surveyresult").length) {
        return $.Deferred().reject("DOM doesn't contain '.js_surveyresult'");
    }

    console.debug(
        "[survey_result_date_filter] Survey Result Date Filter is loading..."
    );

    $(".js_surveyresult #filter_date").click(function() {
        var date_from = $("div#datetimepicker_from")
            .find("input.form-control")
            .val();
        var date_end = $("div#datetimepicker_end")
            .find("input.form-control")
            .val();
        // Find by different date format
        var re_date_from = new RegExp("[&?]date_from=[0-9]*[-./][0-9]*[-./][0-9]*");
        var re_date_end = new RegExp("[&?]date_end=[0-9]*[-./][0-9]*[-./][0-9]*");
        // Add new parameters or update existing ones
        console.debug(document.URL.indexOf("date_from"));
        var URL = document.URL;
        if (URL.indexOf("?date_from") != -1) {
            // Keep ? in case there are more parameters after
            URL = URL.replace(re_date_from, "?");
        } else {
            URL = URL.replace(re_date_from, "");
        }
        if (URL.indexOf("?date_end") != -1) {
            URL = URL.replace(re_date_end, "?");
        } else {
            URL = URL.replace(re_date_end, "");
        }
        // Fix ?& to just ? in case we had more parameters after dates
        URL = URL.replace("?&", "?");
        console.debug("URL => " + URL);
        // Set dates separately in case filtering by only one date
        if (date_from != "") {
            if (URL.indexOf("?") == -1) {
                URL = URL + "?" + encodeURI("date_from" + "=" + date_from);
            } else {
                URL = URL + "&" + encodeURI("date_from" + "=" + date_from);
            }
        }
        if (date_end != "") {
            if (URL.indexOf("?") == -1) {
                URL = URL + "?" + encodeURI("date_end" + "=" + date_end);
            } else {
                URL = URL + "&" + encodeURI("date_end" + "=" + date_end);
            }
        }
        console.debug("Final URL => " + URL);
        window.location.href = URL;
    });

    $(".js_surveyresult .date-range-filter i.fa-calendar").on("click", function(e) {
        // Get date format from attribute in the view
        var date_format = $(this)
            .closest("div.date")
            .find("input")
            .attr("data-date-format");

        console.log("Date Format => " + date_format);
        $(e.currentTarget)
            .closest("div.date")
            .find("input")
            .datetimepicker({
                format: date_format,
                icons: {
                    time: "fa fa-clock-o",
                    date: "fa fa-calendar",
                    up: "fa fa-chevron-up",
                    down: "fa fa-chevron-down",
                },
            });
        $(e.currentTarget)
            .closest("div.date")
            .find("input")
            .datetimepicker("show");
    });

    console.debug("[survey_result_date_filter]  Survey Result Date Filter is loaded!");
});
