import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-survey",
    description="Meta package for oca-survey Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-partner_survey',
        'odoo13-addon-survey_description',
        'odoo13-addon-survey_question_type_five_star',
        'odoo13-addon-survey_resource_booking',
        'odoo13-addon-survey_xlsx',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
