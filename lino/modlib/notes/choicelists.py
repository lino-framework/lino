# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Choicelists for :mod:`lino.modlib.notes`.

.. autosummary::

"""

from lino.api import dd, rt, _


class SpecialType(dd.Choice):
    """Represents a special note type."""

    def get_notes(self, **kw):
        """Return a queryset with the uploads of this shortcut."""
        return rt.modules.notes.Note.objects.filter(
            type__special_type=self, **kw)


class SpecialTypes(dd.ChoiceList):
    """The list of special note types which have been declared on this
    Site.

    """
    verbose_name = _("Special note type")
    verbose_name_plural = _("Special note types")
    item_class = SpecialType
    max_length = 5
