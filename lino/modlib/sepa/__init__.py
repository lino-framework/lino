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

    # import_statements_path = "/home/khchine5/Documents/Documentation/Lino/Ticket 505/test_file/"
    import_statements_path = None
    """A path wildcard pointing to xml files which need to get imported.

    As a system admin you can set this e.g. by specifying in your
    :xfile:`settings.py` (*before* instantiating your
    :setting:`SITE`)::

       ad.configure_plugin('sepa', import_statements_path="/var/sepa")

    End-users are supposed to download SEPA statement files to that
    directory and then to invoke the
    :class:`lino.modlib.sepa.models.ImportStatements` action.

    """

    def setup_main_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('system.SiteConfig', 'import_sepa')

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('sepa.Accounts')
        m.add_action('sepa.Statements')
        m.add_action('sepa.Movements')
