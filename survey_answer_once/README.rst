.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==================
Survey Answer Once
==================

This module extends the functionality of the `survey` module.
It adds a configurable checkbox on a survey so that each user is allowed
to answer it only once.

Usage
=====

To use this module, you need to:

#. Create a survey
#. Use the checkbox to allow answering only once per user.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/200/8.0

Known issues / Roadmap
======================

* Currently only works for logged in users, not for public users.
* Currently only complains at the moment you want to submit for a second time. This is safe, but more user-friendly would be to also show the user on opening of the survey that he has already taken it, and if possible, show him a link to the answer(s) he has given.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/survey/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Dan Kiplangat <dan@sunflowerweb.nl>
* Tom Blauwendraat <info@sunflowerweb.nl>
* Holger Brunn <hbrunn@therp.nl>

Do not contact contributors directly about support or help with technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
