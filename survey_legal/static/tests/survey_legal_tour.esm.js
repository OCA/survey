import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_legal", {
    test: true,
    steps: () => [
        {
            content: "Start Survey",
            trigger: "button.btn:contains('Start Survey')",
            run: "click",
        },
        {
            content: "Answer Where do you live",
            trigger: 'div.js_question-wrapper:contains("Where do you live") input',
            run: "edit Mordor-les-bains",
        },

        {
            content: "Accept legal terms",
            trigger: "input#accepted_legal_terms",
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
