odoo.define(
    "survey_crm_generation.tour_test_survey_crm_generation",
    function (require) {
        "use strict";

        const tour = require("web_tour.tour");

        tour.register(
            "test_survey_crm_generation",
            {
                test: true,
                url: "/survey/start/08b4db21-66cc-4c69-a712-cc364c54902c",
            },
            [
                {
                    content: "Start Survey",
                    trigger: "button.btn:contains('Start Survey')",
                },
                {
                    content: "E-mail address",
                    trigger:
                        "div.js_question-wrapper:contains('E-mail address') textarea",
                    run: "text test@test.com",
                },
                {
                    content: "Your company name?",
                    trigger:
                        "div.js_question-wrapper:contains('Your company name?') textarea",
                    run: "text Tecnativa",
                },
                {
                    content: "And your name?",
                    trigger:
                        "div.js_question-wrapper:contains('And your name?') textarea",
                    run: "text Tecnativa",
                },
                {
                    content: "Referenced by",
                    trigger:
                        "div.js_question-wrapper:contains('Referenced by') span:contains('Other:')",
                },
                {
                    content: "Referenced by: other",
                    trigger:
                        "div.js_question-wrapper:contains('Referenced by') textarea",
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
    }
);
