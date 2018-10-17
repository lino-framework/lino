# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines some system models, especially the :class:`SiteConfig` model.

This plugin is installed in most Lino applications.

.. autosummary::
   :toctree:

   choicelists
   models


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
        from lino.core.utils import models_by_base
        if len(list(models_by_base(site.models.system.Lockable))):
            
            def welcome_messages(ar):
                def fmt(model, pk):
                    try:
                        obj = model.objects.get(pk=pk)
                    except model.DoesNotExist:
                        return "{}{}".format(model.__name__, pk)
                    return ar.obj2html(obj)

                up = ar.get_user().get_preferences()
                if len(up.locked_rows):
                    chunks = [
                        ugettext("You have a dangling edit lock on"), " "]
                    chunks += join_elems(
                        [fmt(m, pk) for m, pk in up.locked_rows], ", ")
                    chunks.append('.')
                    yield E.span(*chunks)


            site.add_welcome_handler(welcome_messages)

