# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Provides a framework for configuring and generating printable
documents called "database excerpts".

- Lino automatically installs a "Print" action on every model of your
  app for which the database contains an :class:`ExcerptType`
  instance.

- Lino does not automatically add an action per model to make the
  excerpt history visible from a model. If you this, add yourself your
  preferred variant. This can be either using a
  :class:`dd.ShowSlaveTable` button in the toolbar::

    show_excerpts = dd.ShowSlaveTable('excerpts.ExcerptsByOwner')
    show_excerpts = dd.ShowSlaveTable('excerpts.ExcerptsByProject')

  Or by adding :class:`excerpts.ExcerptsByOwner <ExcerptsByOwner>` or
  :class:`excerpts.ExcerptsByProject <ExcerptsByProject>` (or both, or
  your own subclass of one of them) to the
  :attr:`detail_layout <dd.Actor.detail_layout>`.


.. autosummary::
   :toctree:

   models
   mixins
   choicelists
   fixtures.std


Document templates
==================

.. xfile:: excerpts/Default.odt

This template is the default value, used by many excerpt types in
their :attr:`ExcerptType.template` field.  It is designed to be
locally overridden by local site administrators in order to match
their letter paper.

"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Excerpts")

    needs_plugins = ['lino.modlib.outbox', 'lino.modlib.office']

    def setup_main_menu(self, site, profile, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('excerpts.MyExcerpts')

    def setup_config_menu(self, site, profile, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('excerpts.ExcerptTypes')

    def setup_explorer_menu(self, site, profile, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('excerpts.Excerpts')
