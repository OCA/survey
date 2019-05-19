import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-survey",
    description="Meta package for oca-survey Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-partner_survey',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
