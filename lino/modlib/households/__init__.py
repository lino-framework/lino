# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Households")
    person_model = "contacts.Person"

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
