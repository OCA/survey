/** @odoo-module */
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_contact_update", {
    steps: () => [
        {
            content: "Click on Start",
            trigger: "button.btn:contains('Start Survey')",
            run: "click",
        },
        {
            content: "Company Name",
            trigger: "div.js_question-wrapper input",
            run: "edit My Updated Company Name",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
            run: "click",
        },
        {
            content: "Name",
            trigger: "div.js_question-wrapper input",
            run: "edit My Updated Name",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
            run: "click",
        },
        {
            content: "Email",
            trigger: "div.js_question-wrapper input",
            run: "edit survey_contact_generation@test.com",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
            run: "click",
        },
        {
            content: "Notes",
            trigger: "div.js_question-wrapper textarea",
            run: "edit This is a test note",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
            run: "click",
        },
        {
            content: "Color",
            trigger: "div.js_question-wrapper input",
            run: "edit 1",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
            run: "click",
        },
        {
            content: "Country",
            trigger:
                "div.js_question-wrapper label:contains('Romania') i.fa-circle-thin",
            run: "click",
        },
        {
            content: "Tags",
            trigger:
                "div.js_question-wrapper label:contains('Prospects') i.fa-square-o",
            run: "click",
        },
        {
            content: "Tags",
            trigger: "div.js_question-wrapper label:contains('Vendor') i.fa-square-o",
            run: "click",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
            run: "click",
        },
        {
            content: "Street",
            trigger: "div.js_question-wrapper input",
            run: "edit Main Street, 42",
        },
        {
            content: "Click Submit",
            trigger: "button[value='finish'].btn-secondary",
            run: "click",
        },
        {
            content: "Thank you",
            trigger: "h1:contains('Thank you!')",
        },
    ],
});
