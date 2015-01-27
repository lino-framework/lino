# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
.. autosummary::
    :toctree:

    models
    utils



"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


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
        m.add_action('accounts.Charts')
        m.add_action('accounts.Groups')
        m.add_action('accounts.Accounts')

