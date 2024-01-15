/** @odoo-module */

import tour from "web_tour.tour";

tour.register(
    "test_survey_dont_skip_start",
    {
        test: true,
        url: "/survey/start/b135640d-14d4-4748-9ef6-344ca256531e",
    },
    [
        {
            content: "Click on Start",
            trigger: "button.btn:contains('Start Survey')",
        },
        {
            content: "And then we fill in the survey...",
            trigger: "div.js_question-wrapper:contains('Where do you live') input",
            run: "text Spain",
        },
    ]
);

tour.register(
    "test_survey_skip_start",
    {
        test: true,
        url: "/survey/start/b135640d-14d4-4748-9ef6-344ca256531e",
    },
    [
        {
            content: "We dive right into the survey form...",
            trigger: "div.js_question-wrapper:contains('Where do you live') input",
            run: "text Spain",
        },
    ]
);
