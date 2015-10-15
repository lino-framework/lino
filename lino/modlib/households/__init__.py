# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for managing households (i.e. groups of humans
who live together in a same house).

Technical specification see :ref:`lino.specs.households`.

.. autosummary::
   :toctree:

    models
    choicelists
    fixtures.std
    fixtures.demo

This plugin is being extended by :ref:`welfare` in
:mod:`lino_welfare.modlib.households`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "Extends :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Households")

    person_model = "contacts.Person"
    """A string referring to the model which represents a human in your
    application.  Default value is ``'contacts.Person'`` (referring to
    :class:`lino.modlib.contacts.models.Person`).

    """

    def setup_main_menu(config, site, profile, m):
        mnugrp = site.plugins.contacts
        m = m.add_menu(mnugrp.app_label, mnugrp.verbose_name)
        m.add_action('households.Households')

    def setup_config_menu(config, site, profile, m):
        mnugrp = site.plugins.contacts
        m = m.add_menu(mnugrp.app_label, mnugrp.verbose_name)
        # m.add_action(Roles)
        m.add_action('households.Types')

    def setup_explorer_menu(config, site, profile, m):
        mnugrp = site.plugins.contacts
        m = m.add_menu(mnugrp.app_label, mnugrp.verbose_name)
        m.add_action('households.MemberRoles')
        m.add_action('households.Members')
