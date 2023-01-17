odoo.define("survey_crm_generation.tour_test_survey_crm_generation", function(require) {
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
                content: "Click on Start",
                trigger: "a.btn:contains('Start')",
            },
            {
                content: "E-mail address",
                trigger: "div.js_question-wrapper:contains('E-mail address') input",
                run: "text test@test.com",
            },
            {
                content: "Your company name?",
                trigger: "div.js_question-wrapper:contains('Your company name?') input",
                run: "text Tecnativa",
            },
            {
                content: "And your name?",
                trigger: "div.js_question-wrapper:contains('And your name?') input",
                run: "text Tecnativa",
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
