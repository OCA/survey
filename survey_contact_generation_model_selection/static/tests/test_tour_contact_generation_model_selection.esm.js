import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_question_model", {
    test: true,
    url: "/survey/start/b137640d-14d4-4748-9ef6-344caaaaaaf",
    steps: () => [
        {
            trigger: 'button.btn.btn-primary.btn-lg:contains("Start Survey")',
        },
        {
            content: "Name",
            trigger: "div.js_question-wrapper input",
            run: "text My Name",
        },
        {
            content: "Email",
            trigger: "div.js_question-wrapper input",
            run: "text survey_contact_generation@test.com",
        },
        {
            // Now click input explicitly
            content: "focus input",
            trigger: "input.survey-model-input",
            run: "click",
        },
        {
            // Wait for dropdown to appear
            content: "wait dropdown",
            trigger: 'li[data-label="Murcia (ES)"]',
            run: "click",
        },
        {
            content: "Click Submit",
            trigger: "button[value='finish'].btn-secondary",
        },
    ],
});
