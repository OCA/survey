import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-survey",
    description="Meta package for oca-survey Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-survey_question_type_five_star',
        'odoo14-addon-survey_question_type_nps',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
