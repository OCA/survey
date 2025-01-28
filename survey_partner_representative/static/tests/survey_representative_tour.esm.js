/** @odoo-module */

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_representative", {
    test: true,
    url: "/survey/start/80e5f1e2-1a9d-4c51-8e23-4abc7534",
    steps: () => [
        {
            content: "Click on Start",
            trigger: 'button.btn:contains("Start")',
        },
        {
            content: "Name",
            trigger: "div.js_question-wrapper:contains('Name') input",
            run: "text Mr. Odoo",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "Email",
            trigger: "div.js_question-wrapper:contains('Email') input",
            run: "text mrodoo@test.com",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "What meal?",
            trigger:
                "div.js_question-wrapper:contains('What would you like for dinner') label:contains('Meat') i",
            run: function () {
                $(
                    "div.js_question-wrapper:contains('What would you like for dinner') label:contains('Meat') i"
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
    ],
});
