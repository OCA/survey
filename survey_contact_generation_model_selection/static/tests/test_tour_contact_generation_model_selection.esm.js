import {registry} from "@web/core/registry";

registry
    .category("web_tour.tours")
    .add("test_tour_contact_generation_model_selection", {
        steps: () => [
            {
                content: "Start Survey",
                trigger: "button.btn:contains('Start Survey')",
                run: "click",
            },
            {
                content: "Name",
                trigger: "div.js_question-wrapper:contains('Name') input",
                run: "edit My Name",
            },
            {
                content: "Email",
                trigger: "div.js_question-wrapper:contains('Email') input",
                run: "edit survey_contact_generation@test.com",
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
                trigger:
                    "div.js_question-wrapper:contains('State') div.choices__inner option:contains('Murcia (ES)'):not(:visible)",
                run: "click",
            },
            {
                content: "Click Submit and finish the survey",
                trigger: 'button[value="finish"]',
                run: "click",
            },
            {
                content: "Modal",
                trigger: "footer:contains('Submit') button.btn-primary",
                run: "click",
            },
            // Final page
            {
                content: "Thank you",
                trigger: 'h1:contains("Thank you!")',
            },
        ],
    });
