# Copyright 2008-2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines a list of languages (the :class:`Language
<lino.modlib.langguages.models.Language>` model).

It is used by :mod:`lino_xl.lib.cv`, whose :class:`LanguageKnowledge
<lino_xl.lib.cv.models.LanguageKnowledge>` and :class:`Schooling
<lino_xl.lib.cv.models.Schooling>` models have a `language` field
which points to this the :class:`Language
<lino.modlib.langguages.models.Language>` model.

Note that this has nothing to do with the list of languages in your
:attr:`languages <lino.core.site.Site.languages>` setting.


.. autosummary::
   :toctree:

    models
    fixtures.few_languages
    fixtures.all_languages

"""
from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Boards")

    def setup_config_menu(self, site, user_type, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('languages.Languages')
