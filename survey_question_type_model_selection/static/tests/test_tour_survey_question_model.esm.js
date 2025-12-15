/** @odoo-module **/
/* Copyright 2025 Tecnativa - Eduardo Ezerouali
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("test_survey_question_model", {
    test: true,
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
            trigger: "button.btn.btn-secondary[type='submit']",
            run: "click",
        },
    ],
});
