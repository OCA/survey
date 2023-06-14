odoo.define("survey.tour_test_survey_contact_generation", function(require) {
    "use strict";

    const tour = require("web_tour.tour");

    tour.register(
        "test_survey_contact_generation",
        {
            test: true,
            url: "/survey/start/80e5f1e2-1a9d-4c51-8e23-09e93f7fa2c5",
        },
        [
            {
                content: "Click on Start",
                trigger: "a.btn:contains('Start')",
            },
            {
                content: "Name",
                trigger: "div.js_question-wrapper:contains('Name') input",
                run: "text My Name",
            },
            {
                content: "Email",
                trigger: "div.js_question-wrapper:contains('Email') input",
                run: "text test@test.com",
            },
            {
                content: "Notes",
                trigger: "div.js_question-wrapper:contains('Notes') textarea",
                run: "text This is a test note",
            },
            {
                content: "Color",
                trigger: "div.js_question-wrapper:contains('Color') input",
                run: "text 1",
            },
            {
                content: "Date",
                trigger: "div.js_question-wrapper:contains('Date') input",
                run: "text 01/01/2023",
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
