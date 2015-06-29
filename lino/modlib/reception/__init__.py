# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This module is for managing a reception desk and a waiting queue:
register clients into a waiting queue as they present themselves at a
reception desk (Empfangsschalter), and unregister them when they leave
again.

It depends on :mod:`lino.modlib.cal`. It does not add any model, but
adds some workflow states, actions and tables.

Extended by :mod:`lino_welfare.modlib.reception`.


.. autosummary::
   :toctree:

    models


"""
from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Reception")

    needs_plugins = ['lino.modlib.system', 'lino.modlib.cal']

    required_user_groups = 'reception'
    """The required user groups for viewing actors of this plugin.
    
    This is overridden by Lino Welfare to include "coaching".

    This way of configuring permissions is an example for why it would
    be useful to replace user groups by a UserProfile class (and to
    populate UserProfiles with subclasses of it).

    """

    def setup_main_menu(config, site, profile, m):
        app = site.plugins.reception
        m = m.add_menu(app.app_name, app.verbose_name)

        m.add_action('cal.EventsByDay')

        m.add_action('reception.WaitingVisitors')
        m.add_action('reception.BusyVisitors')
        m.add_action('reception.GoneVisitors')

        # MyWaitingVisitors is maybe not needed as a menu entry since it
        # is also a get_admin_main_items. if i remove it then i must edit
        # `pcsw_tests.py`.  Waiting for user feedback before doing this.
        m.add_action('reception.MyWaitingVisitors')

