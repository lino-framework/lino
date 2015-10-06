# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Provides a framework for configuring and generating printable
documents called "database excerpts".

See also :doc:`/admin/excerpts`.


Lino does not automatically add an action per model to make the
excerpt history visible from a model. If you want this, add yourself
your preferred variant.

This can be either using a :class:`lino.core.actions.ShowSlaveTable`
button in the toolbar::

    show_excerpts = dd.ShowSlaveTable('excerpts.ExcerptsByOwner')
    show_excerpts = dd.ShowSlaveTable('excerpts.ExcerptsByProject')

Or by adding :class:`excerpts.ExcerptsByOwner <ExcerptsByOwner>` or
:class:`excerpts.ExcerptsByProject <ExcerptsByProject>` (or both, or
your own subclass of one of them) to the :attr:`detail_layout
<lino.core.actors.Actor.detail_layout>`.

.. autosummary::
   :toctree:

   models
   mixins
   choicelists
   fixtures.std
   fixtures.demo2

"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Excerpts")

    needs_plugins = [
        'lino.modlib.printing',
        'lino.modlib.outbox', 'lino.modlib.office']

    # _default_template_handlers = {}

    responsible_user = None
    """The username of the user responsible for monitoring the excerpts
    system. This is currently used only by
    :mod:`lino.modlib.excerpts.fixtures.demo2`.
    """

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
        m.add_action('excerpts.AllExcerpts')

    # def register_default_template_handler(self, model, func):
    #     self._default_template_handlers[model] = func

    # def get_default_template(self, bm, obj):
    #     """Return the filename to use as main template when no
    #     explicit template name is specified.
    #     :attr:`template<lino.modlib.printing.mixins.PrintableType.template>`.

    #     """
    #     h = self._default_template_handlers.get(obj.__class__, None)
    #     if h is None:
    #         return bm.get_default_template(obj)
    #     return h(obj, bm)


# def default_template_handler(obj, bm):
#     if bm.default_template:
#         return bm.default_template
#     return 'Default' + bm.template_ext


