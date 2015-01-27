# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"See :mod:`ml.humanlinks`."

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Parency links")

    ## settings
    person_model = 'contacts.Person'

    def setup_explorer_menu(config, site, profile, m):
        p = site.plugins.contacts
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('humanlinks.Links')
        m.add_action('humanlinks.LinkTypes')


