# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""The top-level plugin for doing accounting stuff with a Lino
application.

.. autosummary::
    :toctree:

    choicelists
    models
    utils
    fields

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Accounting")

    ref_length = 20
    """The `max_length` of the `Reference` field of an account.
    """

    def __init__(self, *args):
        super(Plugin, self).__init__(*args)
        if hasattr(self.site, 'accounts_ref_length'):
            v = self.site.accounts_ref_length
            raise Exception("""%s has an attribute 'accounts_ref_length'!.
You probably want to replace this by:
ad.configure_plugins("accounts", ref_length=%r)
""" % (self.site, v))

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('accounts.AccountCharts')
        if False:
            for ch in site.modules.accounts.AccountCharts.items():
                m.add_action(
                    site.modules.accounts.GroupsByChart, master_instance=ch)
        m.add_action('accounts.Groups')
        m.add_action('accounts.Accounts')

