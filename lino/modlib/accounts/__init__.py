# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""

.. setting:: accounts.ref_length

The max_length of reference fields

"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Accounting")

    ref_length = 20

    def __init__(self, *args):
        super(Plugin, self).__init__(*args)
        if hasattr(self.site, 'accounts_ref_length'):
            v = self.site.accounts_ref_length
            raise Exception("""%s has an attribute 'accounts_ref_length'!.
You probably want to replace this by:
ad.configure_plugins("accounts", accounts_ref_length=%r)
""" % (self.site, v))

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('accounts.Charts')
        m.add_action('accounts.Groups')
        m.add_action('accounts.Accounts')

