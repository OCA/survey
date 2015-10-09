[![Runbot Status](https://runbot.odoo-community.org/runbot/badge/flat/200/8.0.svg)](https://runbot.odoo-community.org/runbot/repo/github-com-oca-survey-200)
[![Build Status](https://travis-ci.org/OCA/survey.svg?branch=8.0)](https://travis-ci.org/OCA/survey)
[![Coverage Status](https://coveralls.io/repos/OCA/survey/badge.svg?branch=8.0)](https://coveralls.io/r/OCA/survey?branch=8.0)
[![Code Climate](https://codeclimate.com/github/OCA/survey/badges/gpa.svg)](https://codeclimate.com/github/OCA/survey)

OCA Survey management addons for Odoo
=====================================

This project aims to deal with modules related to survey management.


What is survey
--------------

Odoo includes basic functionality with the survey module.
Historic features have been removed from the official code gradually as major versions.
This repository aims to consolidate community efforts around extended features.

In the field of FOSS, if you do not need to interact directly with other Odoo features, you should see alternatives like https://www.limesurvey.org


Roadmap
-------

- add new type of answer. For example "percent" type : one respondent is asked how to spread his activity as a percentage from a preconfigured list pending precise values. Workaround : If no requirement for precise value, it can be configured ranges of values in a list of choices.
- allow adding comment on each item for multiple choice answer
- format "date time" type to set date and time or only date or only time
- allow subquestions. Very useful with conditional_questions to loop on a page or series of questions
- allow editing or inserting Odoo blocks in website survey inside of the question-answer group and not only around or after.  For example, one respondent is asked to vote about pictures selection.
- offer choice to the survey's administrator to display information from an existing object (for example : res.partner)
- extend the existing notation to finely evaluate or profile by answering and generate actions (for example : generate sale order and sale order lines depending on respondent answers)


Links
-----

https://github.com/ingadhoc/odoo-addons/tree/8.0/survey_conditional_questions

https://github.com/csrocha/openerp-survey


[//]: # (addons)
Available addons
----------------
addon | version | summary
--- | --- | ---
[partner_survey](partner_survey/) | 8.0.1.0.0 | Partner Survey

[//]: # (end addons)

Translation Status
------------------
[![Transifex Status](https://www.transifex.com/projects/p/OCA-survey-8-0/chart/image_png)](https://www.transifex.com/projects/p/OCA-survey-8-0)
