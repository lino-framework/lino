# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Choicelists for `lino.modlib.ledger`.

"""

from django.conf import settings

from lino.api import dd, rt, _


class FiscalYear(dd.Choice):
    pass


class FiscalYears(dd.ChoiceList):

    """A list of the fiscal years available in this database.

    The default value for this list is 5 years starting from
    :attr:`lino.core.site.Site.start_year`.  If the fiscal year of
    your company is the same as the calendar year, then the default
    entries in this should do.  Otherwise you can always override this
    in your :meth:`lino.core.site.Site.setup_choicelists`.

    """
    item_class = FiscalYear
    verbose_name = _("Fiscal Year")
    verbose_name_plural = _("Fiscal Years")
    # ~ preferred_width = 4 # would be 2 otherwise

    @classmethod
    def from_int(cls, year):
        return cls.get_by_value(str(year)[2:])

    @classmethod
    def from_date(cls, date):
        return cls.from_int(date.year)

for y in range(settings.SITE.start_year, dd.today().year + 5):
    s = str(y)
    FiscalYears.add_item(s[2:], s)


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
    """A list of the available voucher types (i.e. the database models
subclasses of ledger.Voucher`).

    """

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


