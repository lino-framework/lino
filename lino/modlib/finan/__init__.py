# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds functionality for managing financial stuff.

.. autosummary::
   :toctree:

    models
    choicelists
    mixins

"""

from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Financial")

    needs_plugins = ['lino.modlib.ledger']

    # def setup_main_menu(self, site, profile, m):
    #     m = m.add_menu(self.app_label, self.verbose_name)
    #     ledger = site.modules.ledger
    #     for jnl in ledger.Journal.objects.filter(trade_type=''):
    #         m.add_action(jnl.voucher_type.table_class,
    #                      label=unicode(jnl),
    #                      params=dict(master_instance=jnl))

    def setup_explorer_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('finan.BankStatements')
        m.add_action('finan.JournalEntries')
        m.add_action('finan.PaymentOrders')
        m.add_action('finan.Groupers')
