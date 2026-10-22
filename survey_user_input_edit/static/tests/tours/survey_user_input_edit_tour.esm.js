import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_user_input_edit", {
    url: "/survey/start/test_survey_user_input_edit_token",
    steps: () => [
        {
            content: "Click on Start Survey",
            trigger: 'button.btn.btn-primary.btn-lg:contains("Start Survey")',
            run: "click",
        },
        {
            content: "Answer text question",
            trigger: "div.js_question-wrapper input",
            run: "edit Initial Answer",
        },
        {
            content: "Submit survey",
            trigger: 'button[value="finish"]',
            run: "click",
        },
        {
            content: "Confirm submit in modal",
            trigger: ".modal-footer button.btn-primary",
            run: "click",
        },
        {
            content: "Check Edit your answers button is present on completion screen",
            trigger: 'a.btn.btn-primary.btn-lg:contains("Edit your answers")',
            run: "click",
            expectUnloadPage: true,
        },

        {
            content: "Verify prefilled answer",
            trigger: "div.js_question-wrapper input:value(Initial Answer)",
            run: "edit Updated Answer",
        },
        {
            content: "Resubmit modified survey",
            trigger: 'button[value="finish"]',
            run: "click",
        },
        {
            content: "Confirm resubmit in modal",
            trigger: ".modal-footer button.btn-primary",
            run: "click",
        },
        {
            content: "Check survey is finished again",
            trigger: 'a.btn.btn-primary.btn-lg:contains("Edit your answers")',
        },
    ],
});
