/** @odoo-module */

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_crm_question_model", {
    test: true,
    url: "/survey/start/b137640d-14d4-4748-9ef6-344caaaaaafff",
    steps: () => [
        {
            content: "Start Survey",
            trigger: "button.btn:contains('Start Survey')",
            run: "click",
        },
        {
            content: "Name",
            trigger:
                "div.js_question-wrapper:contains('Name') input, div.js_question-wrapper:contains('Name') textarea",
            run: "text Tecnativa",
        },
        {
            content: "Email",
            trigger:
                "div.js_question-wrapper:contains('Email') input, div.js_question-wrapper:contains('Email') textarea",
            run: "text test@test.com",
        },
        {
            content: "Open dropdown",
            trigger: ".choices, .choices__inner",
            run: "click",
        },
        // WAIT OPTION LIST (no separate waiting-only step)
        {
            content: "Select option 62",
            trigger: ".choices__list--dropdown .choices__item--choice[data-value='62']",
            run: "click",
            extra_trigger:
                ".choices__list--dropdown.is-active, .choices__list--dropdown",
        },
        {
            content: "Click Submit",
            trigger: "button[value='finish']",
            run: "click",
        },
        {
            content: "Thank you",
            trigger: "div.o_survey_finished",
        },
    ],
});
