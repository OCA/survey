import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_crm_question_model", {
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
            run: "edit Tecnativa",
        },
        {
            content: "Email",
            trigger:
                "div.js_question-wrapper:contains('Email') input, div.js_question-wrapper:contains('Email') textarea",
            run: "edit test@test.com",
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
        },
        {
            content: "Click Submit",
            trigger: "button[value='finish']",
            run: "click",
        },
        {
            content: "Modal",
            trigger: "footer:contains('Submit') button.btn-primary",
            run: "click",
        },
        {
            content: "Thank you",
            trigger: "div.o_survey_finished",
        },
    ],
});
