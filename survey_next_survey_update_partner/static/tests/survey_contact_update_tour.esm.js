/** @odoo-module */
import tour from "web_tour.tour";

tour.register(
    "test_survey_contact_update",
    {
        test: true,
    },
    [
        {
            content: "Click on Start",
            trigger: "button.btn:contains('Start Survey')",
        },
        {
            content: "Name",
            trigger: "div.js_question-wrapper:contains('Name') input",
            run: "text My Updated Name",
        },
        {
            content: "Company Name",
            trigger: "div.js_question-wrapper:contains('Company name') input",
            run: "text My Updated Company Name",
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
            content: "Street",
            trigger: "div.js_question-wrapper:contains('Street') input",
            run: "text Main Street, 42",
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
