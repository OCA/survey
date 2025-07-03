odoo.define("suvey_previous_page_skip_validation.form", function (require) {
    "use strict";

    var SurveyForm = require("survey.form");

    SurveyForm.include({
        _submitForm: function (options) {
            if (options.previousPageId) {
                options.skipValidation = true;
            }
            this._super.apply(this, arguments);
        },
    });

    return SurveyForm;
});
