# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Choicelists for `lino.modlib.ledger`.

"""

from lino.api import dd, rt


class VoucherType(dd.Choice):

    def __init__(self, model, table_class):
        self.table_class = table_class
        model = dd.resolve_model(model)
        self.model = model
        value = dd.full_model_name(model)
        text = model._meta.verbose_name + ' (%s)' % dd.full_model_name(model)
        # text = model._meta.verbose_name + ' (%s.%s)' % (
        #     model.__module__, model.__name__)
        name = None
        super(VoucherType, self).__init__(value, text, name)

    def get_journals(self):
        return rt.modules.ledger.Journal.objects.filter(voucher_type=self)


class VoucherTypes(dd.ChoiceList):
    item_class = VoucherType
    max_length = 100

    @classmethod
    def get_for_model(self, model):
        for o in self.objects():
            # ~ o.model = dd.resolve_model(o.model) # TODO: resolve only once
            if o.model is model:
                return o

    @classmethod
    def add_item(cls, model, table_class):
        return cls.add_item_instance(VoucherType(model, table_class))


