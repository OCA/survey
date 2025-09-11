/** @odoo-module */

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_sale_generation", {
    test: true,
    url: "/survey/start/08b4db20-65cc-4c68-a711-cc364c54901b",
    steps: () => [
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
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "E-mail address",
            trigger: "div.js_question-wrapper:contains('E-mail address') input",
            run: "text test@test.com",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "How many hours will you hire monthly?",
            trigger:
                "div.js_question-wrapper:contains('How many hours will you hire monthly?') input",
            run: "text 3",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "Choose your subscription level",
            trigger:
                "div.js_question-wrapper:contains('Choose your subscription level') span:contains('Gold')",
        },
        {
            content: "Choose your extras",
            trigger:
                "div.js_question-wrapper:contains('Choose your extras') span:contains('Advanced Backup')",
        },
        {
            content: "Choose your extras",
            trigger:
                "div.js_question-wrapper:contains('Choose your extras') span:contains('Mail Management')",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
        },
        {
            content: "Referenced by",
            trigger:
                "div.js_question-wrapper:contains('Referenced by') span:contains('Other:')",
        },
        {
            content: "Referenced by: other",
            trigger: "div.js_question-wrapper textarea",
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
    ],
});
