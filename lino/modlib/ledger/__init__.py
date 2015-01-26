# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This is Lino's standard app for General Ledger.  It defines the
following classes:

.. autosummary::
    :toctree:

    models

- Models :class:`Journal`, :class:`Voucher` and :class:`Movement`

- The :class:`DueMovement` class, a volatile object representing a
  group of matching movements.

- :class:`DebtsByAccount` and :class:`DebtsByPartner` are two reports
  based on :class:`ExpectedMovements`

- :class:`GeneralAccountsBalance`, :class:`ClientAccountsBalance` and
  :class:`SupplierAccountsBalance` three reports based on
  :class:`AccountsBalance` and :class:`PartnerAccountsBalance`

- :class:`Debtors` and :class:`Creditors` are tables with one row for
  each partner who has a positive balance (either debit or credit).
  Accessible via :menuselection:`Reports --> Ledger --> Debtors` and
  :menuselection:`Reports --> Ledger --> Creditors`



.. setting:: ledger.use_pcmn

Whether to use the PCMN notation.

PCMN stands for "plan compatable minimum normalisé" and is a
standardized nomenclature for accounts used in France and Belgium.

"""

from __future__ import unicode_literals


from django.utils.translation import ugettext_lazy as _

from lino import ad


class Plugin(ad.Plugin):
    verbose_name = _("Ledger")
    use_pcmn = False

    def setup_main_menu(config, site, profile, main):
        from lino.modlib.vat.models import TradeTypes
        Journal = site.modules.ledger.Journal
        for tt in TradeTypes.objects():
            m = main.add_menu(tt.name, tt.text)
            for jnl in Journal.objects.filter(trade_type=tt):
                m.add_action(jnl.voucher_type.table_class,
                             label=unicode(jnl),
                             params=dict(master_instance=jnl))

    def setup_reports_menu(self, site, profile, m):
        mg = site.plugins.accounts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('ledger.Situation')
        m.add_action('ledger.ActivityReport')
        m.add_action('ledger.Debtors')
        m.add_action('ledger.Creditors')

    def setup_config_menu(self, site, profile, m):
        mg = site.plugins.accounts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('ledger.Journals')

    def setup_explorer_menu(self, site, profile, m):
        mg = site.plugins.accounts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('ledger.Invoices')
        m.add_action('ledger.Vouchers')
        m.add_action('ledger.VoucherTypes')
        m.add_action('ledger.Movements')
        m.add_action('ledger.FiscalYears')


