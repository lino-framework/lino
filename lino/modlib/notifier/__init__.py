# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for managing notifications.

.. autosummary::
   :toctree:

    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Notifications")

    needs_plugins = ['lino.modlib.users', 'lino.modlib.gfks']

    email_subject_template = "Notification about {obj.owner}"
    """The template used to build the subject lino of notification emails.

    :obj: is the :class:`Notification
          <lino.modlib.notify.models.Notification>` object.

    """

    # def setup_main_menu(self, site, profile, m):
    #     p = site.plugins.office
    #     m = m.add_menu(p.app_label, p.verbose_name)
    #     m.add_action('notifier.MyNotifications')

    def setup_explorer_menu(self, site, profile, m):
        p = site.plugins.system
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('notifier.AllNotifications')
