odoo.define("survey.tour_test_survey_contact_generation", function (require) {
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
                trigger: "button.btn:contains('Start Survey')",
            },
            {
                content: "Name",
                trigger: "div.js_question-wrapper:contains('Name') input",
                run: "text My Name",
            },
            {
                content: "Company Name",
                trigger: "div.js_question-wrapper:contains('Company name') input",
                run: "text My Company Name",
            },
            {
                content: "Email",
                trigger: "div.js_question-wrapper:contains('Email') input",
                run: "text survey_contact_generation@test.com",
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
                content: "Country",
                trigger:
                    "div.js_question-wrapper:contains('Country') label:contains('Romania') i",
                run: function () {
                    $(
                        "div.js_question-wrapper:contains('Country') label:contains('Romania') i"
                    ).prop("checked", true);
                },
            },
            {
                content: "Tags",
                trigger:
                    "div.js_question-wrapper:contains('Tags') label:contains('Prospects') i",
                run: function () {
                    $(
                        "div.js_question-wrapper:contains('Tags') label:contains('Prospects') i"
                    ).prop("checked", true);
                },
            },
            {
                content: "Tags",
                trigger:
                    "div.js_question-wrapper:contains('Tags') label:contains('Vendor') i",
                run: function () {
                    $(
                        "div.js_question-wrapper:contains('Tags') label:contains('Vendor') i"
                    ).prop("checked", true);
                },
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
