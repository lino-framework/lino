# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
The :xfile:`models.py` module for the :mod:`lino.modlib.auto.sales` app.

"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)

import os
import datetime

from django.db import models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode 
from django.utils.functional import lazy

from django.contrib.contenttypes.models import ContentType

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation

from decimal import Decimal

ZERO = Decimal()


#~ from lino import reports
from lino import dd
from lino.utils import AttrDict
from lino.utils.xmlgen.html import E

from lino.core import dbtables

#~ sales = dd.resolve_app('sales')
contacts = dd.resolve_app('contacts')

#~ dd.extends_app('lino.modlib.sales',globals())

from lino.modlib.sales.models import *
#~ PARENT_APP = 'lino.modlib.sales'

#~ from lino.modlib.sales import models as PARENT_APP
#~ from lino.modlib.sales import models as sales
#~ from lino.modlib.sales import models as CONFIG_PARENT
#~ CONFIG_PARENT = sales # inherit `config` subdir


class Invoiceable(dd.Model):
    """
    Mixin for things that are "invoiceable", i.e. for which a customer
    is going to get an invoice.
    """
    invoiceable_date_field = ''
    """
    The name of the field which holds the invoiceable date.
    """
    
    #~ invoiceable_partner_field = ''
    #~ """
    #~ The name of the field which holds the invoiceable partner.
    #~ """
    
    class Meta:
        abstract = True
        
    invoice = dd.ForeignKey('sales.Invoice',
        #~ verbose_name=_("Invoice"),
        blank=True,null=True)

    @classmethod
    def get_partner_filter(cls,partner):
        """
        Return a dict of filter...
        """
        raise NotImplementedError()
        #~ kw = dict()
        #~ kw.update(invoice__isnull=True)
        #~ kw.update(partner=partner)
        #~ return models.Q(**kw)
        
    def get_invoiceable_product(self): return None
    def get_invoiceable_qty(self): return None
    def get_invoiceable_title(self): return unicode(self)
    def get_invoiceable_amount(self): return None
        
    @classmethod
    def get_invoiceables_for(cls,partner,max_date=None):
        if settings.SITE.site_config.site_company:
            if partner.id == settings.SITE.site_config.site_company.id:
                return
        #~ logger.info('20130711 get_invoiceables_for (%s,%s)', partner, max_date)
        for m in dd.models_by_base(cls):
            flt = m.get_partner_filter(partner)
            #~ fkw = dict()
            #~ fkw[m.invoiceable_partner_field] = partner
            #~ fkw.update(invoice__isnull=True)
            #~ if max_date is not None:
                #~ fkw["%s__lte" % m.invoiceable_date_field] = max_date
            #~ logger.info('20130711 %s %s', m, fkw)
            qs = m.objects.filter(flt)
            #~ qs = qs.exclude(company=settings.SITE.site_config.site_company)
            for obj in qs.order_by(m.invoiceable_date_field):
                if obj.get_invoiceable_product() is not None:
                    yield obj
        
    @classmethod
    def unused_get_invoiceables_count(cls,partner,max_date=None):
        if settings.SITE.site_config.site_company:
            if partner.id == settings.SITE.site_config.site_company.id:
                return 0
        #~ logger.info('20130711 get_invoiceables_count (%s,%s)', partner, max_date)
        n = 0
        for m in dd.models_by_base(cls):
            flt = m.get_partner_filter(partner)
            qs = m.objects.filter(flt)
            #~ qs = qs.exclude(company=settings.SITE.site_config.site_company)
            n += qs.count()
        return n

def create_invoice_for(obj,ar):
    invoiceables = list(Invoiceable.get_invoiceables_for(obj))
    if len(invoiceables) == 0:
        raise Warning(_("No invoiceables found for %s.") % obj)
    jnl = Invoice.get_journals()[0]
    invoice = Invoice(partner=obj,journal=jnl,date=datetime.date.today())
    invoice.save()
    for ii in invoiceables:
        i = InvoiceItem(voucher=invoice,invoiceable=ii,
            product=ii.get_invoiceable_product(),
            title=ii.get_invoiceable_title(),
            qty=ii.get_invoiceable_qty())
        #~ i.product_changed(ar)
        i.set_amount(ar,ii.get_invoiceable_amount())
        i.full_clean()
        i.save()
    invoice.compute_totals()
    invoice.save()
    return invoice
        
class CreateInvoiceForPartner(dd.Action):
    icon_name = 'money'
    sort_index = 50
    label = _("Create invoice")
    help_text = _("Create invoice for this partner using invoiceable items")
    #~ show_in_row_actions = True
    show_in_workflow = True
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        def ok():
            invoice = create_invoice_for(obj,ar)
            return ar.goto_instance(invoice,**kw)
        if True: # no confirmation
            return ok()
        msg = _("This will create an invoice for %s.") % obj
        return ar.confirm(ok, msg, _("Are you sure?"))
        
        
#~ dd.inject_action('contacts.Partner','create_invoice',CreateInvoiceForPartner())
contacts.Partner.create_invoice = CreateInvoiceForPartner()


    
class Invoice(Invoice): # 20130709
    
    #~ fill_invoice = FillInvoice()
    
    class Meta(Invoice.Meta): # 20130709
        #~ app_label = 'sales'
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
        
    def register(self,ar):
        for i in self.items.filter(invoiceable_id__isnull=False):
            if i.invoiceable.invoice != self:
                i.invoiceable.invoice = self
                i.invoiceable.save()
                #~ logger.info("20130711 %s now invoiced",i.invoiceable)
        return super(Invoice,self).register(ar)
        
    def deregister(self,ar):
        for i in self.items.filter(invoiceable_id__isnull=False):
            if i.invoiceable.invoice != self:
                logger.warning("Oops: i.invoiceable.invoice != self in %s",self)
            i.invoiceable.invoice = None
            i.invoiceable.save()
            #~ logger.info("20130711 %s no longer invoiced",i.invoiceable)
        return super(Invoice,self).deregister(ar)
        
    def get_invoiceables(self,model):
        lst = []
        for i in self.items.all():
            if isinstance(i.invoiceable,model):
                if not i.invoiceable in lst:
                    lst.append(i.invoiceable)
            #~ else:
                #~ print 20130910, i.invoiceable.__class__
        return lst
                    
                
    def get_build_method(self):
        return 'appypdf' # must be appypdf for print_multiple
    
class InvoiceItem(InvoiceItem): # 20130709
    
    invoiceable_label = _("Invoiceable")
    
    class Meta(InvoiceItem.Meta): # 20130709
        #~ app_label = 'sales'
        verbose_name = _("Voucher item")
        verbose_name_plural = _("Voucher items")
    
    
    invoiceable_type = dd.ForeignKey(ContentType,
        editable=False,blank=True,null=True,
        verbose_name=string_concat(invoiceable_label,' ',_('(type)')))
    invoiceable_id = dd.GenericForeignKeyIdField(
        invoiceable_type,
        editable=False,blank=True,null=True,
        verbose_name=string_concat(invoiceable_label,' ',_('(object)')))
    invoiceable = dd.GenericForeignKey(
        'invoiceable_type', 'invoiceable_id',
        verbose_name=invoiceable_label)
        
    #~ def product_changed(self,ar):
        #~ super(InvoiceItem,self).product_changed(ar)
        #~ if self.invoiceable:
            #~ self.title = self.invoiceable.get_invoiceable_title()
        
    
class ItemsByInvoice(ItemsByInvoice): # 20130709
    #~ app_label = 'sales' # we want to "override" the original table

    column_names = "invoiceable product title description:20x1 discount unit_price qty total_incl total_base total_vat"
    
    #~ @classmethod
    #~ def get_choices_text(self,obj,request,field):
        #~ if field.name == 'enrolment':
            #~ return unicode(obj.course)
        #~ # raise Exception("20130607 field.name is %r" % field.name)
        #~ return super(ItemsByInvoice,self).get_choices_text(obj,field,request)
    
class InvoicingsByInvoiceable(InvoiceItemsByProduct): # 20130709
    label = _("Invoicings")
    #~ app_label = 'sales'
    master_key = 'invoiceable'
    editable = False
    column_names = "voucher qty title description:20x1 discount unit_price total_incl total_base total_vat"
    
    #~ column_names = 
    
#~ sales.ItemsByInvoice.column_names = "enrolment product title description:20x1 discount unit_price qty total_incl total_base total_vat"
    


#~ contacts = dd.resolve_app('contacts')


#~ class InvoiceablePartners(contacts.Partners):
    #~ """
    #~ TODO: read https://docs.djangoproject.com/en/dev/topics/db/aggregation/
    #~ """
    #~ label = _("Invoiceable partners")
    #~ help_text = _("Table of all partners who have at least one invoiceable item.")
    #~ model = 'contacts.Partner'
    #~ create_invoice = CreateInvoiceForPartner()
    #~ 
    #~ @classmethod
    #~ def get_request_queryset(self,ar):
        #~ qs = super(InvoiceablePartners,self).get_request_queryset(ar)
        #~ flt = Q()
        #~ for m in dd.models_by_base(Invoiceable):
            #~ subquery = m.objects.filter(invoice__isnull=True).values(m.invoiceable_partner_field+'__id')
            #~ flt = flt | Q(id__in=subquery)
        #~ return qs.filter(flt)
        #~ 
        
class CreateInvoice(CreateInvoiceForPartner):
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        ar.selected_rows = [ o.partner for o in ar.selected_rows ]
        return super(CreateInvoice,self).run_from_ui(ar,**kw)
        
from lino.mixins.printable import CachedPrintAction

    
class CreateAllInvoices(CachedPrintAction):
    #~ icon_name = 'money'
    
    #~ label = _("Create invoices")
    help_text = _("Create and print the invoice for each selected row, making these rows disappear from this table")
    
    def run_from_ui(self,ar,**kw):
        #~ obj = ar.selected_rows[0]
        #~ assert obj is None
        def ok():
            invoices = []
            for row in ar.selected_rows:
                partner = contacts.Partner.objects.get(pk=row.pk)    
                invoice = create_invoice_for(partner,ar)
                invoices.append(invoice)
            #~ for obj in ar:
                #~ invoice = create_invoice_for(obj.partner,ar)
                #~ invoices.append(invoice)
            mf = self.print_multiple(ar,invoices)
            kw.update(open_url=mf.url)
            kw.update(refresh_all=True)
            return kw
        #~ msg = _("This will create and print %d invoices.") % ar.get_total_count()
        msg = _("This will create and print %d invoice(s).") % len(ar.selected_rows)
        return ar.confirm(ok, msg, _("Are you sure?"))

    
        
    
min_amount = Decimal()

class InvoicesToCreate(dd.VirtualTable):
    label = _("Invoices to create")
    cell_edit = False
    help_text = _("Table of all partners who should receive an invoice.")
    issue_invoice = CreateInvoice()
    column_names = "first_date last_date partner amount action_buttons"
    create_all_invoices = CreateAllInvoices()

    
    @classmethod
    def get_data_rows(self,ar):
        qs = contacts.Partner.objects.all()
        if ar.quick_search is not None:
            qs = dbtables.add_quick_search_filter(qs,ar.quick_search)
        if ar.gridfilters is not None:
            qs = dbtables.add_gridfilters(qs,ar.gridfilters)
        
        rows = []
        for p in qs:
            row = self.get_row_for(p)
            if row.amount >= min_amount and row.first_date is not None:
                rows.append(row)
        
        def f(a,b): return cmp(a.first_date,b.first_date)
        rows.sort(f)
        return rows
        
    @classmethod
    def get_row_for(self,partner):
        invoiceables = list(Invoiceable.get_invoiceables_for(partner))
        amount = Decimal()
        first_date = last_date = None
        for i in invoiceables:
            am = i.get_invoiceable_amount()
            if am is not None:
                amount += am
            d = getattr(i,i.invoiceable_date_field)
            if d is not None:
                if first_date is None or d < first_date: first_date = d
                if last_date is None or d > last_date: last_date = d
        return AttrDict(
            id=partner.id,
            pk=partner.pk,
            first_date=first_date,
            last_date=last_date,
            partner=partner,
            amount=amount,
            invoiceables=invoiceables)
                
    @classmethod
    def get_pk_field(self):
        #~ print 20130831,repr(contacts.Partner._meta.pk)
        return contacts.Partner._meta.pk
        
    @classmethod
    def get_row_by_pk(self,ar,pk):
        partner = contacts.Partner.objects.get(pk=pk)
        return self.get_row_for(partner)
        
    @dd.virtualfield(models.DateField(_("First date")))
    def first_date(self,row,ar):
        return row.first_date
    
    @dd.virtualfield(models.DateField(_("Last date")))
    def last_date(self,row,ar):
        return row.last_date
    
    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount(self,row,ar):
        return row.amount
    
    @dd.virtualfield(models.ForeignKey('contacts.Partner'))
    def partner(self,row,ar):
        return row.partner
    
    @dd.displayfield(_("Invoiceables"))
    def unused_invoiceables(self,row,ar):
        items = []
        for i in row.invoiceables:
            items += [ar.obj2html(i),' ']
        return E.p(*items)
        
    @dd.displayfield(_("Actions"))
    def action_buttons(self,obj,ar):
        # must override because the action is on obj.partner, not on obj
        return obj.partner.show_invoiceables.as_button(ar)
        #~ return obj.partner.create_invoice.as_button(ar)
        
        
      
        
    

    
    
    
    
class InvoiceablesByPartner(dd.VirtualTable):
    icon_name = 'money'
    sort_index = 50
    label = _("Invoices to create")
    #~ label = _("Invoiceables")
    help_text = _("List of invoiceable items for this partner")

    #~ app_label = 'sales'
    master = 'contacts.Partner'
    column_names = 'date info'
    
    @classmethod
    def get_data_rows(self,ar):
        rows = []
        mi = ar.master_instance
        if mi is None:
            return rows
        for obj in Invoiceable.get_invoiceables_for(mi):
            rows.append((getattr(obj,obj.invoiceable_date_field),obj))
        
        #~ for m in dd.models_by_base(Invoiceable):
            #~ fkw = {m.invoiceable_partner_field:mi}
            #~ for obj in m.objects.filter(**fkw).order_by(m.invoiceable_date_field):
                #~ rows.append((getattr(obj,m.invoiceable_date_field),obj))
        def f(a,b): return cmp(a[0],b[0])
        rows.sort(f)
        return rows
        
    @dd.virtualfield(models.DateField(_("Date")))
    def date(self,row,ar):
        return row[0]
    
    @dd.displayfield(_("Invoiceable"))
    def info(self,row,ar):
        return ar.obj2html(row[1])
    
contacts.Partner.show_invoiceables = dd.ShowSlaveTable(InvoiceablesByPartner)



#~ f = setup_main_menu
def setup_main_menu(site,ui,profile,m): 
    #~ f(site,ui,profile,m)
    m = m.add_menu("sales",MODULE_LABEL)
    #~ m.add_action('sales.InvoiceablePartners')
    m.add_action('sales.InvoicesToCreate')
