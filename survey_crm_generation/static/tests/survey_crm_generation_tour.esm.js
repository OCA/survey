/** @odoo-module */

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_crm_generation", {
    test: true,
    url: "/survey/start/08b4db21-66cc-4c69-a712-cc364c54902c",
    steps: () => [
        {
            content: "Start Survey",
            trigger: "button.btn:contains('Start Survey')",
        },
        {
            content: "E-mail address",
            trigger: "div.js_question-wrapper:contains('E-mail address') textarea",
            run: "text test@test.com",
        },
        {
            content: "Continue",
            trigger: "button.btn:contains('Continue')",
        },
        {
            content: "Your company name?",
            trigger: "div.js_question-wrapper:contains('Your company name?') textarea",
            run: "text Tecnativa",
        },
        {
            content: "Continue",
            trigger: "button.btn:contains('Continue')",
        },
        {
            content: "And your name?",
            trigger: "div.js_question-wrapper:contains('And your name?') textarea",
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
    ],
});
