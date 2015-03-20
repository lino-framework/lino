# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for handling plausibility problems.

A plausibility problem is a "soft" database integrity problem which is
not visible by the DBMS because detecting it requires higher business
intelligence.  This is what they have in common with repairable
problems (defined using the :class:`Repairable
<lino.mixins.repairable.Repairable>` mixin). Unlike repairable
problems, plausibility problems cannot be fixed automatically,
i.e. they need **human interaction**.

The application developer writes **plausibility checkers**,
i.e. pieces of code which contain that business intelligence and which
are attached to a given model.

Examples of plausibility problems are:

- :class:`lino_welfare.modlib.pcsw.models.SSINChecker`
- :class:`lino_welfare.modlib.pcsw.models.ClientCoachingsChecker`
- :class:`lino_welfare.modlib.isip.mixins.OverlappingContractsChecker`
- :class:`lino_welfare.modlib.dupable_clients.models.SimilarClientsChecker`

Users automatically get a button "Update plausibility problems" on
objects for which there is at least one checker available.

The application developer can also add a :class:`ProblemsByOwner`
table to the `detail_layout` of any model.


.. autosummary::
   :toctree:

    models
    choicelists
    fixtures.demo2
    management.commands.check_plausibility

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    """See :doc:`/dev/plugins`.

    """
    verbose_name = _("Plausibility")

    needs_plugins = ['lino.modlib.contenttypes']

    def setup_main_menu(self, site, profile, m):
        g = site.plugins.office
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('plausibility.MyProblems')

    def setup_explorer_menu(config, site, profile, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('plausibility.Checkers')
        m.add_action('plausibility.AllProblems')
        # m.add_action('plausibility.Severities')
        # m.add_action('plausibility.Feedbacks')

