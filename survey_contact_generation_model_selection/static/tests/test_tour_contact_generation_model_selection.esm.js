/** @odoo-module **/

import {registry} from "@web/core/registry";

registry
    .category("web_tour.tours")
    .add("test_survey_contact_generation_model_selection", {
        test: true,
        steps: () => [
            {
                content: "Start",
                trigger: 'button.btn:contains("Start")',
            },
            {
                content: "Name",
                trigger: "div.js_question-wrapper:contains('Name') input",
                run: "text My Name",
            },
            {
                content: "Email",
                trigger: "div.js_question-wrapper:contains('Email') input",
                run: "text survey_contact_generation@test.com",
            },
            {
                // Now click input explicitly
                content: "focus input",
                trigger: "div.js_question-wrapper:contains('State') div.choices",
                run: "click",
            },
            {
                // Wait for dropdown to appear
                content: "wait dropdown",
                trigger: "div.choices__item--selectable:contains('Murcia (ES)')",
                run: "click",
            },
            {
                content: "Click Submit",
                trigger: "button[value='finish'].btn-secondary",
            },
        ],
    });
