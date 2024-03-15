odoo.define("survey.tour_test_survey_sale_generation", function (require) {
    "use strict";

    const tour = require("web_tour.tour");

    tour.register(
        "test_survey_sale_generation",
        {
            test: true,
            url: "/survey/start/08b4db20-65cc-4c68-a711-cc364c54901b",
        },
        [
            {
                content: "Start Survey",
                trigger: "button.btn:contains('Start Survey')",
            },
            {
                content: "Name",
                trigger: "div.js_question-wrapper:contains('Name') input",
                run: "text Mr. Odoo",
            },
            {
                content: "E-mail address",
                trigger: "div.js_question-wrapper:contains('E-mail address') input",
                run: "text test@test.com",
            },
            {
                content: "How many hours will you hire monthly?",
                trigger:
                    "div.js_question-wrapper:contains('How many hours will you hire monthly?') input",
                run: "text 3",
            },
            {
                content: "Choose your subscription level",
                trigger:
                    "div.js_question-wrapper:contains('Choose your subscription level') span:contains('Gold')",
            },
            {
                content: "Add advanced backup",
                trigger:
                    "div.js_question-wrapper:contains('Choose your extras') span:contains('Advanced Backup')",
            },
            {
                content: "Add mail management",
                trigger:
                    "div.js_question-wrapper:contains('Choose your extras') span:contains('Mail Management')",
            },
            {
                content: "Referenced by",
                trigger:
                    "div.js_question-wrapper:contains('Referenced by') span:contains('Other:')",
            },
            {
                content: "Referenced by: other",
                trigger: "div.o_survey_comment_container textarea",
                run: "text Mr. Odoo",
            },
            {
                content: "Click Submit",
                trigger: "button[value='finish']",
            },
            {
                content: "Thank you",
                trigger: "h1:contains('Thank you!')",
            },
        ]
    );
});
