# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from djangosite.dbutils import models_by_base

from lino.utils import mti
from lino.utils import join_elems
from lino.utils.xmlgen.html import E
from lino.core import model
from lino.core import fields


class Polymorphic(model.Model):

    """Mixin for models that use Multiple Table Inheritance to implement
    polymorphism.  Subclassed e.g. by
    :class:`ml.contacts.Partner`. The recipient of an invoice can be
    either a person or a company, a client, a job provider, an
    employee...). A given partner can be both a person and an employee
    at the same time.

    TODO: Rename this to Polymorphic.  Because this is not used by
    e.g. :class:`ml.ledger.Voucher` because a voucher has a pointer to
    the journal which knows which specialization to use.  A given
    voucher has always exactly one specialization.

    """
    class Meta:
        abstract = True

    # def get_child_model(self):
    #     return self.__class__

    # def get_mti_leaf(self):
    #     model = self.get_child_model()
    #     if model is self.__class__:
    #         return self
    #     related_name = model.__name__.lower()
    #     return getattr(self, related_name)

    def get_mti_child(self, *args):
        """Return the specified specialization or `None`.

        For example if you have two models `Place(Model)` and
        `Restaurant(Place)` and a `Place` instance ``p`` which is
        *not* also a Restaurant, then `p.get_mti_child('restaurant')`
        will return `None`.

        """
        for a in args:
            try:
                return getattr(self, a)
            except ObjectDoesNotExist:
                pass
        #~ return self

    # def insert_child(self, *args, **attrs):
    #     return insert_child(self, *args, **attrs)

    _mtinav_models = None

    @classmethod
    def on_analyze(cls, site):
        if cls._mtinav_models is None:
            cls._mtinav_models = tuple(models_by_base(cls))

    def get_mti_buttons(self, ar):
        forms = []
        for m in self._mtinav_models:
            if self.__class__ is m:
                forms.append(unicode(m._meta.verbose_name))
            else:
                obj = mti.get_child(self, m)
                if obj is not None:
                    forms.append(ar.obj2html(obj, m._meta.verbose_name))
        return forms
