import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_representative", {
    steps: () => [
        {
            content: "Click on Start",
            trigger: 'button.btn:contains("Start")',
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
            content: "Email",
            trigger: "div.js_question-wrapper:contains('Email') input",
            run: "edit mrodoo@test.com",
        },
        {
            content: "Submit and go to Next Page",
            trigger: 'button[value="next"]',
            run: "click",
        },
        {
            content: "What meal?",
            trigger:
                "div.js_question-wrapper:contains('What would you like for dinner') label:contains('Meat') i",
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
            trigger: "h1:contains('Thank you!')",
        },
    ],
});
