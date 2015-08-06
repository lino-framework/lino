# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This is Lino's standard plugin for General Ledger.

.. autosummary::
    :toctree:

    utils
    choicelists
    roles
    mixins
    models

"""

from __future__ import unicode_literals

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Ledger")

    needs_plugins = ['lino.modlib.accounts']

    use_pcmn = False
    """
    Whether to use the PCMN notation.

    PCMN stands for "plan compatable minimum normalisé" and is a
    standardized nomenclature for accounts used in France and Belgium.

    """

    project_model = None
    """Leave this to `None` for normal behaviour.  Set this to a string of
    the form `'<app_label>.<ModelName>'` if you want to add an
    additional field `project` to all models which inherit from
    :class:`lino.modlib.ledger.mixins.ProjectRelated`.

    """

    intrusive_menu = False
    """Whether the plugin should integrate into the application's main
    menu in an intrusive way.  Intrusive means that the main menu gets
    one top-level item per journal group.

    The default behaviour is `False`, meaning that these items are
    gathered below a single item "Accounting".

    """
    
    def setup_main_menu(self, site, profile, m):
        if not self.intrusive_menu:
            mg = site.plugins.accounts
            m = m.add_menu(mg.app_label, mg.verbose_name)

        Journal = site.modules.ledger.Journal
        JournalGroups = site.modules.ledger.JournalGroups
        for grp in JournalGroups.objects():
            subm = m.add_menu(grp.name, grp.text)
            for jnl in Journal.objects.filter(journal_group=grp):
                subm.add_action(jnl.voucher_type.table_class,
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
        m.add_action('ledger.PaymentTerms')

    def setup_explorer_menu(self, site, profile, m):
        mg = site.plugins.accounts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('ledger.MatchRules')
        m.add_action('ledger.Vouchers')
        m.add_action('ledger.VoucherTypes')
        m.add_action('ledger.Movements')
        m.add_action('ledger.FiscalYears')
        m.add_action('ledger.TradeTypes')


