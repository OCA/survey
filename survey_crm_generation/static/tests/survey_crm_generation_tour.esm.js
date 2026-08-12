import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_crm_generation", {
    steps: () => [
        {
            content: "Start Survey",
            trigger: "button.btn:contains('Start Survey')",
            run: "click",
        },
        {
            content: "E-mail address",
            trigger: "div.js_question-wrapper:contains('E-mail address') textarea",
            run: "edit test@test.com",
        },
        {
            content: "Continue",
            trigger: "button.btn:contains('Continue')",
            run: "click",
        },
        {
            content: "Your company name?",
            trigger: "div.js_question-wrapper:contains('Your company name?') textarea",
            run: "edit Tecnativa",
        },
        {
            content: "Continue",
            trigger: "button.btn:contains('Continue')",
            run: "click",
        },
        {
            content: "And your name?",
            trigger: "div.js_question-wrapper:contains('And your name?') textarea",
            run: "edit Tecnativa",
        },
        {
            content: "Continue",
            trigger: "button.btn.btn-primary[type='submit']",
            run: "click",
        },
        {
            content: "Referenced by",
            trigger:
                "div.js_question-wrapper:contains('Referenced by') span:contains('Other:')",
            run: "click",
        },
        {
            content: "Referenced by: other",
            trigger: "div.js_question-wrapper:contains('Referenced by') textarea",
            run: "edit Mr. Odoo",
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
