# -*- coding: UTF-8 -*-
# Copyright 2010-2018 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This package contains model mixins, some of which are heavily used
by applications and the :ref:`xl`. But none of them is mandatory.

.. autosummary::
   :toctree:

    duplicable
    dupable
    sequenced
    human
    periods
    polymorphic
    uploadable
"""

from __future__ import unicode_literals
from builtins import str

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.functions import Length

from etgen.html import E
from lino.core import model
from lino.core.fields import displayfield

class Referrable(model.Model):
    """
    Mixin for things that have a unique reference, i.e. an identifying
    name used by humans to refer to an individual object.

    A reference, unlike a primary key, can easily be changed.

    .. attribute:: ref

        The reference. This must be either empty or unique.
    """
    class Meta(object):
        abstract = True

    ref_max_length = 40
    """The maximum length of the :attr:`ref` field."""

    ref = models.CharField(
        _("Reference"), max_length=ref_max_length,
        blank=True, null=True, unique=True)

    def on_duplicate(self, ar, master):
        """
        Before saving a duplicated object for the first time, we must
        change the :attr:`ref` in order to avoid an IntegrityError.
        """
        if self.ref:
            self.ref += ' (DUP)'
        super(Referrable, self).on_duplicate(ar, master)

    @classmethod
    def get_by_ref(cls, ref, default=models.NOT_PROVIDED):
        """
        Return the object identified by the given reference.
        """
        try:
            return cls.objects.get(ref=ref)
        except cls.DoesNotExist:
            if default is models.NOT_PROVIDED:
                raise cls.DoesNotExist(
                    "No %s with reference %r" % (str(cls._meta.verbose_name), ref))
            return default

    @classmethod
    def quick_search_filter(cls, search_text, prefix=''):
        """Overrides the default behaviour defined in
        :meth:`lino.core.model.Model.quick_search_filter`. For
        Referrable objects, when quick-searching for a text containing
        only digits, the user usually means the :attr:`ref` and *not*
        the primary key.

        """
        #if search_text.isdigit():
        if search_text.startswith('*'):
            return models.Q(**{prefix+'ref__icontains': search_text[1:]})
        return super(Referrable, cls).quick_search_filter(search_text, prefix)


class StructuredReferrable(Referrable):
    class Meta:
        abstract = True
        
    @classmethod
    def get_usable_items(cls):
        return cls.objects.annotate(
            ref_len=Length('ref')).filter(
                ref_len=cls.ref_max_length)
    
    def get_choices_text(self, request, actor, field):
        return "{} {}".format(self.ref, self)

    def is_heading(self):
        return len(self.ref) < self.__class__.ref_max_length

    @displayfield(_("Description"), max_length=50)
    def description(self, ar):
        s = self.ref
        s = u' ' * (len(s)-1) + s
        s += " " + str(self)
        if self.is_heading():
            s = E.b(s)
        return s

    
