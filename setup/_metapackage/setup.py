import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-survey",
    description="Meta package for oca-survey Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-survey_conditional_question',
        'odoo14-addon-survey_description',
        'odoo14-addon-survey_multiple_choice_max_answer',
        'odoo14-addon-survey_question_type_binary',
        'odoo14-addon-survey_question_type_five_star',
        'odoo14-addon-survey_question_type_nps',
        'odoo14-addon-survey_text_question_validation_length',
        'odoo14-addon-survey_xlsx',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
