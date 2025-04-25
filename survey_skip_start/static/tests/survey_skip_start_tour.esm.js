/** @odoo-module **/

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_skip_start", {
    test: true,
    url: "/survey/start/b135640d-14d4-4748-9ef6-344ca256531e",
    steps: () => [
        {
            content: "Answer Where do you live",
            trigger: 'div.js_question-wrapper:contains("Where do you live") input',
            run: "text Spain",
        },
    ],
});
