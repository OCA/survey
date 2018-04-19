import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-survey",
    description="Meta package for oca-survey Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-partner_survey',
        'odoo8-addon-survey_one_choice_per_column',
        'odoo8-addon-survey_partner_tag_share',
        'odoo8-addon-survey_percent_question',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
