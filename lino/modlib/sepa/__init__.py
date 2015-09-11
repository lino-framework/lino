# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds models and tables for managing bank accounts for your
partners.  It requires the :mod:`lino.modlib.contacts` app.

.. autosummary::
   :toctree:

    models
    ui
    mixins
    utils
    fields
    fixtures.demo
    fixtures.sample_ibans

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("SEPA")
    site_js_snippets = ['iban/uppercasetextfield.js']

    import_statements_path = "/home/luc/tmp"
    # import_statements_path = None
    """A path wildcard pointing to xml files which need to get imported.

    End-users will download SEPA statement files to that directory.

    The :class:`lino.modlib.sepa.models.ImportStatements` action
    imports fiels from this location.

    """

    def setup_main_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('system.SiteConfig', 'import_sepa')

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('sepa.Accounts')
