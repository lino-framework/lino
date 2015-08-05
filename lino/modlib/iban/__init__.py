# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds models and tables for managing bank accounts for your
partners.  It requires the :mod:`lino.modlib.contacts` app.

.. autosummary::
   :toctree:

    models
    mixins
    utils


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("IBAN")
    site_js_snippets = ['iban/uppercasetextfield.js']
