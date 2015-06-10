# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.vat`.

This module defines some central ChoiceLists and Model mixins designed
to work both with and without :mod:`lino.modlib.ledger` installed.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

from django.db import models
from django.conf import settings

from lino.api import dd
from django.utils.translation import ugettext_lazy as _

partner_model = settings.SITE.partners_app_label + '.Partner'

vat = dd.resolve_app('vat')
ledger = dd.resolve_app('ledger')


ZERO = Decimal()


# class DeclarationStates(dd.Workflow):
#     pass
# add = DeclarationStates.add_item
# add("00", _("Draft"), "draft", editable=True)
# add("10", _("Registered"), "registered", editable=False)
# add("20", _("Submitted"), "submitted", editable=False)

# DeclarationStates.registered.add_transition(
#     _("Register"), states='draft submitted')
# DeclarationStates.draft.add_transition(_("Deregister"), states="registered")
# DeclarationStates.submitted.add_transition(_("Submit"), states="registered")


from dateutil.relativedelta import relativedelta


class DeclarationPeriods(dd.ChoiceList):
    verbose_name = _("VAT Period")
    verbose_name_plural = _("VAT Periods")

    @classmethod
    def setup_field(cls, fld):
        def d():
            return cls.from_date(settings.SITE.today())
        fld.default = d

    @classmethod
    def from_date(cls, date):
        date -= relativedelta(months=1)
        return cls.from_int(date.month)

    @classmethod
    def from_int(cls, month):
        return cls.get_by_value('%02d' % month)


add = DeclarationPeriods.add_item

if settings.SITE.plugins.vat.vat_quarterly:

    add('Q1', _("First Quarter (January-March)"), months=(1, 2, 3))
    add('Q2', _("Second Quarter (April-June)"), months=(4, 5, 6,))
    add('Q3', _("Third Quarter (July-August)"), months=(7, 8, 9))
    add('Q4', _("Fourth Quarter (September-December)"), months=(10, 11, 12))

else:

    add('01', _("January"), 'january', months=(1,))
    add('02', _("February"), 'february', months=(2,))
    add('03', _("March"), 'march', months=(3,))
    add('04', _("April"), 'april', months=(4,))
    add('05', _("May"), 'may', months=(5,))
    add('06', _("June"), 'june', months=(6,))
    add('07', _("July"), 'july', months=(7,))
    add('08', _("August"), 'august', months=(8,))
    add('09', _("September"), 'september', months=(9,))
    add('10', _("October"), 'october', months=(10,))
    add('11', _("November"), 'november', months=(11,))
    add('12', _("December"), 'december', months=(12,))


from .be import DeclarationFields


#~ class Declarable(dd.Model):
    #~ class Meta:
        #~ abstract = True
    #~ declaration = models.ForeignKey('declarations.Declaration',
        #~ blank=True,null=True)

    #~ def can_declare(self,decl):
        #~ if self.number is None: return False
        #~ if self.year != decl.year: return False
        #~ if not self.date.month in decl.period.months: return False
        #~ return True

def collect_declared_values(jnl, mvt, decl, sums):
    #~ logger.info("20121208 %s in %s",doc.date.month,self.period.months)
    #~ tt = self.get_trade_type()
    for fld in DeclarationFields.get_list_items():
        amount = fld.amount_for_field(decl, mvt, jnl)
        if amount:
            sums[fld.name] += amount

    return None


class Declaration(ledger.Voucher):

    """
    A VAT declaration is when a company declares to the state
    how much sales and purchases they've done during a given period.
    It is a summary of ledger movements.
    It is at the same time a ledger voucher.
    """

    #~ fields_list = DeclarationFields

    class Meta:
        verbose_name = _("VAT declaration")
        verbose_name_plural = _("VAT declarations")

    #~ year = FiscalYears.field()
    period = DeclarationPeriods.field()
    # state = DeclarationStates.field(default=DeclarationStates.draft)

    #~ def save(self,*args,**kw):
        #~ if self.state == DeclarationStates.draft:
            #~ if self.year and self.period:
                #~ self.compute_fields()
        #~ super(Declaration,self).save(*args,**kw)

    def full_clean(self, *args, **kw):
        self.compute_fields()
        super(Declaration, self).full_clean(*args, **kw)

    def before_state_change(self, ar, old, new):
        if new.name == 'register':
            self.compute_fields()
        elif new.name == 'draft':
            for doc in ledger.Voucher.objects.filter(declared_in=self):
                doc.declared_in = None
                doc.save()
        super(Declaration, self).before_state_change(ar, old, new)

    #~ def register(self,ar):
        #~ self.compute_fields()
        #~ super(Declaration,self).register(ar)
        #~
    #~ def deregister(self,ar):
        #~ for doc in ledger.Voucher.objects.filter(declared_in=self):
            #~ doc.declared_in = None
            #~ doc.save()
        #~ super(Declaration,self).deregister(ar)
    def compute_fields(self):
        sums = dict()
        for fld in DeclarationFields.objects():
            sums[fld.name] = ZERO

        count = 0
        for jnl in ledger.Journal.objects.exclude(trade_type=''):

            #~ for doc in ledger.Voucher.objects.filter(
                #~ journal=jnl,declaration__isnull=True,number__isnull=False
                #~ ):

            for month in self.period.months:
                #~ Join on field 'date' not permitted. Did you misspell 'month' for the lookup type?
                for mvt in ledger.Movement.objects.filter(
                    voucher__journal=jnl,
                    voucher__year=self.year,
                    voucher__date__month=month,
                    voucher__declared_in__isnull=True
                ):

                    #~ logger.info("20121208 a can_declare %s",doc)
                    collect_declared_values(jnl, mvt, self, sums)

                for doc in ledger.Voucher.objects.filter(
                    journal=jnl,
                    year=self.year,
                    date__month=month,
                    declared_in__isnull=True
                ):

                    #~ logger.info("20121208 a can_declare %s",doc)
                    count += 1
                    doc.declared_in = self
                    doc.save()
                    #~ declared_docs.append(doc)

        #~ print 20121209, item_models
        #~ for m in item_models:
        #~ for m in rt.models_by_base(VatDocument):
            #~ for item in m.objects.filter(voucher__declaration=self):
                #~ logger.info("20121208 b document %s",doc)
                #~ self.collect_item(sums,item)

        for fld in DeclarationFields.get_list_items():
            setattr(self, fld.name, sums[fld.name])


    #~ def collect_item(self,sums,item):
        #~ tt = item.voucher.get_trade_type()
        #~ for fld in DeclarationFields.objects():
            #~ amount = fld.amount_for_field(self,item,tt)
            #~ if amount:
                #~ sums[fld.name] += amount

            #~ m = getattr(self,"collect_"+fld.name,None)
            #~ if m:
                #~ amount = m(self,tt,doc)
                #~ if amount:
                    #~ sums[fld.name] += amount


class VouchersByDeclaration(ledger.Vouchers):
    #~ master = Declaration
    #~ column_names = 'date partner journal voucher total_base total_vat total_incl'
    #~ model = VatDocument
    master_key = 'declared_in'
    order_by = ['number']
    editable = False

    #~ @classmethod
    #~ def get_data_rows(self,ar):
        #~ docs = []
        #~ for doc in ledger.Voucher.objects.filter(declared_in=ar.master_instance).order_by('number'):
            #~ docs.append(doc)

        #~ def f(a,b): return cmp(a.date,b.date)
        #~ docs.sort(f)
        #~ return docs

    #~ @dd.virtualfield(models.DateField(_("Date")))
    #~ def date(self,obj,ar=None): return obj.date

    #~ @dd.virtualfield(models.ForeignKey(partner_model))
    #~ def partner(self,obj,ar=None): return obj.partner

    #~ @dd.virtualfield(dd.PriceField(_("Total incl. VAT")))
    #~ def total_incl(self,obj,ar=None): return obj.total_incl

    #~ @dd.virtualfield(dd.PriceField(_("Total excl. VAT")))
    #~ def total_base(self,obj,ar=None): return obj.total_base

    #~ @dd.virtualfield(dd.PriceField(_("Total VAT")))
    #~ def total_vat(self,obj,ar=None): return obj.total_vat

    #~ @dd.displayfield(_("Journal"))
    #~ def journal(self,obj,ar): return obj.journal.href_to(ar)

    #~ @dd.displayfield(_("Voucher"))
    #~ def voucher(self,obj,ar): return obj.href_to(ar)


for fld in DeclarationFields.objects():
    dd.inject_field(Declaration, fld.name,
                    dd.PriceField(fld.text, default=Decimal))


class Declarations(dd.Table):
    model = Declaration
    column_names = 'year period workflow_buttons * state id'
    insert_layout = dd.FormLayout("""
    date 
    year 
    period
    """, window_size=(40, 'auto'))
    detail_layout = dd.FormLayout("""
    date year period user workflow_buttons
    fields
    VouchersByDeclaration
    """, fields=DeclarationFields.fields_layout)


class DeclarationsByJournal(ledger.ByJournal, Declarations):
    params_panel_hidden = True
    #master = journals.Journal
    column_names = "number period date user *"


def customize_ledger():

    dd.inject_field('ledger.Voucher',
                    'declared_in',
                    models.ForeignKey(Declaration,
                                      blank=True, null=True))

customize_ledger()


ledger.VoucherTypes.add_item(Declaration, DeclarationsByJournal)
