/** @odoo-module **/

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_skip_start", {
    test: true,
    steps: () => [
        {
            content: "Answer Where do you live",
            trigger: 'div.js_question-wrapper:contains("Where do you live") input',
            run: "text Spain",
        },
    ],
});
