# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Survey record generation",
    "summary": "Allow to create record of any model when user responds to a survey",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Elabore, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "category": "",
    "depends": ["survey"],
    "data": [
        "security/ir.model.access.csv",
        "views/survey_survey_views.xml",
        "views/survey_question_views.xml",
        "views/survey_user_input_views.xml",
        "views/survey_generated_record_views.xml",
    ],
    "installable": True,
}
