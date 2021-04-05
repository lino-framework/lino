# -*- coding: UTF-8 -*-
# Copyright 2015-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Adds functionality for handling data problems.

See :doc:`/specs/checkdata`.

.. autosummary::
   :toctree:

    roles
    fixtures.checkdata
    management.commands.checkdata

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    """The config descriptor for this plugin.

    .. attribute:: responsible_user

        The :attr:`username <lino.modlib.users.User.username>`
        of the **main checkdata responsible**, i.e. a designated
        user who will be attributed to data problems for which
        no *specific responible* could be designated (returned by the
        checker's :meth:`get_responsible_user
        <lino.modlib.checkdata.choicelists.Checker.get_responsible_user>`
        method).

        The default value for this is `None`, except on a demo site
        (i.e. which has :attr:`is_demo_site
        <lino.core.site.Site.is_demo_site>` set to `True`) where it is
        ``"'robin'``.

    """
    verbose_name = _("Checkdata")
    needs_plugins = ['lino.modlib.users', 'lino.modlib.gfks']

    # plugin settings
    responsible_user = None  # the username (a string)
    _responsible_user = None  # the cached User object

    def get_responsible_user(self, checker, obj):
        if self.responsible_user is None:
            return None
        if self._responsible_user is None:
            User = self.site.models.users.User
            try:
                self._responsible_user = User.objects.get(
                    username=self.responsible_user)
            except User.DoesNotExist:
                msg = "Invalid username '{0}' in `responsible_user` "
                msg = msg.format(self.responsible_user)
                raise Exception(msg)
        return self._responsible_user

    def on_plugins_loaded(self, site):
        """Set :attr:`responsible_user` to ``"'robin'`` if this is a demo site
        (:attr:`is_demo_site <lino.core.site.Site.is_demo_site>`).

        """
        super(Plugin, self).on_plugins_loaded(site)
        if site.is_demo_site:
            self.configure(responsible_user='robin')

    def post_site_startup(self, site):
        super(Plugin, self).post_site_startup(site)
        site.models.checkdata.Checkers.sort()

    def setup_main_menu(self, site, user_type, m):
        g = site.plugins.office
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('checkdata.MyProblems')

    def setup_explorer_menu(config, site, user_type, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('checkdata.Checkers')
        m.add_action('checkdata.AllProblems')
        # m.add_action('checkdata.Severities')
        # m.add_action('checkdata.Feedbacks')

    def get_requirements(self, site):
        yield "schedule"
