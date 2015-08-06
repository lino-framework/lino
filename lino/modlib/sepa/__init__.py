# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds models and tables for managing bank accounts for your
partners.  It requires the :mod:`lino.modlib.contacts` app.

.. autosummary::
   :toctree:

    models
    mixins
    utils
    fields

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("SEPA")
    site_js_snippets = ['iban/uppercasetextfield.js']

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('sepa.Accounts')
