odoo.define("survey_signature.print", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");
    var dom = require("web.dom");

    publicWidget.registry.SurveyPrintWidget = publicWidget.Widget.extend({
        selector: ".o_survey_print",

        // --------------------------------------------------------------------------
        // Widget
        // --------------------------------------------------------------------------

        /**
         * @override
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // Will allow the textarea to resize if any carriage return instead of showing scrollbar.
                self.$("textarea").each(function () {
                    dom.autoresize($(this));
                });

                self.$(".o_signature_container").each(function () {
                    $(this).find(".card-header").css("display", "none");
                    var data = $(this).data("value");

                    if (data) {
                        var image = new Image();

                        image.src = "data:image/png;base64," + data.split("'")[1];
                        $(this).find(".signature").append(image);
                    }
                });
            });
        },
    });

    return publicWidget.registry.SurveyPrintWidget;
});
