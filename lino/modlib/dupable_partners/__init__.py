# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for avoiding duplicate partner records.

To use it, applications must do two things:

- add the following line to their :meth:`get_installed_apps
  <lino.core.site.Site.get_installed_apps>`::

    yield 'lino.modlib.dupable_partners'

- Override their :class:`contacts.Partner
  <lino.modlib.contacts.models.Partner>` model to inherit from
  :class:`lino.modlib.dupable_partners.mixins.DupablePartner`.

Defines a virtual slave table :class:`SimilarPartners`, which shows
the partners that are "similar" to a given master instance (and
therefore are potential duplicates).

See also :mod:`lino.mixins.dupable`.

A usage example is :mod:`lino.projects.min2`.
See also :mod:`lino_welfare.modlib.dupable_clients`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Dupable partners")

    needs_plugins = ['lino.modlib.contacts']

    def setup_explorer_menu(self, site, profile, main):
        mg = site.plugins.contacts
        m = main.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('dupable_partners.Words')
        
