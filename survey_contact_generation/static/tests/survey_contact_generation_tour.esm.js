/** @odoo-module */

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_contact_generation", {
    test: true,
    url: "/survey/start/80e5f1e2-1a9d-4c51-8e23-09e93f7fa2c5",
    steps: () => [
        {
            content: "Click on Start",
            trigger: "button.btn:contains('Start Survey')",
        },
        {
            content: "Company Name",
            trigger: "div.js_question-wrapper input",
            run: "text My Company Name",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "Name",
            trigger: "div.js_question-wrapper input",
            run: "text My Name",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "Email",
            trigger: "div.js_question-wrapper input",
            run: "text survey_contact_generation@test.com",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "Notes",
            trigger: "div.js_question-wrapper textarea",
            run: "text This is a test note",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "Color",
            trigger: "div.js_question-wrapper input",
            run: "text 1",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "Date",
            trigger: "div.js_question-wrapper input",
            run: "text 01/01/2023",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "Country",
            trigger:
                "div.js_question-wrapper label:contains('Romania') i.fa-circle-thin",
        },
        {
            content: "Tags",
            trigger: "div.js_question-wrapper label:contains('Prospects') i",
        },
        {
            content: "Tags",
            trigger: "div.js_question-wrapper label:contains('Vendor') i",
        },
        {
            content: "Click Submit",
            trigger: "button[value='finish'].btn-secondary",
        },
        {
            content: "Thank you",
            trigger: "h1:contains('Thank you!')",
        },
    ],
});
