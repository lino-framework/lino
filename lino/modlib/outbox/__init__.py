# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"See :mod:`ml.outbox`."

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Outbox")

    needs_plugins = ['lino.modlib.uploads']

    MODULE_LABEL = _("Outbox")

    def setup_main_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('outbox.MyOutbox')

    def setup_explorer_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('outbox.Mails')
        m.add_action('outbox.Attachments')


