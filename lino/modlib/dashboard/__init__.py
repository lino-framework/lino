# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Adds the *dashboard items* to the *user preferences* so that users
can individually customize their dashboard.

See :doc:`/specs/dashboard`.

.. autosummary::
   :toctree:

    models
"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Dashboard")

    needs_plugins = ['lino.modlib.users']

    def setup_explorer_menu(self, site, user_type, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('dashboard.AllWidgets')

    def setup_user_prefs(self, up):
        if not up.user.is_authenticated:
            return
        qs = self.site.models.dashboard.Widget.objects.filter(
            user=up.user, visible=True).order_by('seqno')
        if qs.count() == 0:
            # print("20161126 no widgets for %s" % up.user)
            return
        lst = []
        d = { i.name: i for i in up.dashboard_items }
        for widget in qs:
            i = d.get(widget.item_name, None)
            if i is None:
                # may be None if dashboard item of that name no
                # longer exists
                pass
                # self.site.logger.warning("20161126")
            else:
                lst.append(i)
        up.dashboard_items = lst
