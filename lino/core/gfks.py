# Copyright 2010-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""A collection of utilities which require Django settings to be
importable.

This defines some helper classes like

- :class:`Parametrizable` and :class:`Permittable` ("mixins" with
  common functionality for both actors and actions),
- the volatile :class:`InstanceAction` object
- the :class:`ParameterPanel` class (used
  e.g. by :class:`lino.mixins.periods.ObservedPeriod`)
- :attr:`ContentType` and `GenericForeignKey`

"""

from __future__ import unicode_literals

from django.conf import settings
from django.db.models import ForeignKey

from .utils import UnresolvedField, UnresolvedModel

if settings.SITE.is_installed('contenttypes'):
    from django.contrib.contenttypes.models import ContentType
    from lino.modlib.gfks.fields import GenericForeignKey
    from django.contrib.contenttypes.fields import GenericForeignKey \
        as DjangoGenericForeignKey

    from django.contrib.contenttypes.fields import GenericRelation

    def is_foreignkey(fld):
        return isinstance(fld, (ForeignKey, DjangoGenericForeignKey))
else:
    ContentType = UnresolvedModel
    GenericForeignKey = UnresolvedField
    GenericRelation = UnresolvedField

    def is_foreignkey(fld):
        return isinstance(fld, ForeignKey)


def gfk2lookup(gfk, obj, **kw):
    """Return a `dict` with the lookup keywords for the given
    GenericForeignKey field `gfk` on the given database object `obj`.

    See also :ref:`book.specs.gfks`.

    """
    if obj is None:
        # 20120222 : here was only `pass`, and the two other lines
        # were uncommented. don't remember why I commented them out.
        # But it caused all tasks to appear in UploadsByController of
        # an insert window for uploads.
        kw[gfk.ct_field] = None
        kw[gfk.fk_field] = None
    else:
        ct = ContentType.objects.get_for_model(obj.__class__)
        kw[gfk.ct_field] = ct
        if not isinstance(obj.pk, (int, long)):
            # IntegerField gives `long` when using MySQL
            return kw
        kw[gfk.fk_field] = obj.pk
    return kw


