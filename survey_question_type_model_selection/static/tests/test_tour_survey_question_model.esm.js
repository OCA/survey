/* Copyright 2025 Tecnativa - Eduardo Ezerouali
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_question_model", {
    url: "/survey/start/b137640d-14d4-4748-9ef6-344caaaaaaf",
    steps: () => [
        {
            trigger: 'button.btn.btn-primary.btn-lg:contains("Start Survey")',
            run: "click",
        },
        {
            content: "focus input",
            trigger: ".choices",
            run: "click",
        },
        {
            content: "wait dropdown list",
            trigger: ".choices__list--dropdown.is-active",
        },
        {
            content: "wait dropdown",
            trigger: ".choices__item--choice[data-value='449']",
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
        {
            content: "Thank you",
            trigger: 'h1:contains("Thank you!")',
        },
    ],
});
