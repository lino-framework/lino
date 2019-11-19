# Copyright 2014-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines some "system features", especially the :class:`SiteConfig` model.
See :doc:`/specs/system`.


"""

from lino import ad, _
from django.utils.translation import ugettext
from etgen.html import E, join_elems



class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("System")

    needs_plugins = ['lino.modlib.printing']

    def setup_config_menu(self, site, user_type, m):
        system = m.add_menu(self.app_label, self.verbose_name)
        system.add_instance_action(site.site_config)


    def on_site_startup(self, site):
        super(Plugin, self).on_site_startup(site)

        from lino.modlib.system.mixins import Lockable

        if len(list(Lockable.get_lockables())):
            def welcome_messages(ar):
                locked_rows = list(Lockable.get_lockable_rows(ar.get_user()))
                if locked_rows:
                    chunks = [
                        ugettext("You have a dangling edit lock on"), " "]
                    chunks += join_elems(
                        [ar.obj2html(obj) for obj in locked_rows], ", ")
                    chunks.append('.')
                    yield E.div(*chunks)

            site.add_welcome_handler(welcome_messages)
