import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_sale_generation", {
    steps: () => [
        {
            content: "Start Survey",
            trigger: "button.btn:contains('Start Survey')",
            run: "click",
        },
        {
            content: "Name",
            trigger: "div.js_question-wrapper:contains('Name') input",
            run: "edit Mr. Odoo",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
            run: "click",
        },
        {
            content: "E-mail address",
            trigger: "div.js_question-wrapper:contains('E-mail address') input",
            run: "edit test@test.com",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
            run: "click",
        },
        {
            content: "How many hours will you hire monthly?",
            trigger:
                "div.js_question-wrapper:contains('How many hours will you hire monthly?') input",
            run: "edit 3",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
            run: "click",
        },
        {
            content: "Choose your subscription level",
            trigger:
                "div.js_question-wrapper:contains('Choose your subscription level') span:contains('Gold')",
            run: "click",
        },
        {
            content: "Choose your extras",
            trigger:
                "div.js_question-wrapper:contains('Choose your extras') span:contains('Advanced Backup')",
            run: "click",
        },
        {
            content: "Choose your extras",
            trigger:
                "div.js_question-wrapper:contains('Choose your extras') span:contains('Mail Management')",
            run: "click",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
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
            trigger: "div.js_question-wrapper textarea",
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
