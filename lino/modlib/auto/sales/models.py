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

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import os

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


#~ from lino import reports
from lino import dd

#~ sales = dd.resolve_app('sales')
#~ contacts = dd.resolve_app('contacts')

from lino.modlib.sales.models import *
#~ from lino.modlib.sales import models as sales
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
    
    invoiceable_partner_field = ''
    """
    The name of the field which holds the invoiceable partner.
    """
    
    class Meta:
        abstract = True
        
    invoiced = dd.ForeignKey('sales.Invoice',
        #~ verbose_name=_("Invoice"),
        blank=True,null=True)

    def get_invoiceable_product(self): return None
    def get_invoiceable_qty(self): return None
    def get_invoiceable_title(self): return unicode(self)
        
    @classmethod
    def get_invoiceables_for(cls,partner,max_date=None):
        for m in dd.models_by_base(cls):
            fkw = dict()
            fkw[m.invoiceable_partner_field] = partner
            fkw.update(invoiced__isnull=True)
            if max_date is not None:
                fkw["%s__lte" % m.invoiceable_date_field] = max_date
            for obj in m.objects.filter(**fkw).order_by(m.invoiceable_date_field):
                yield obj
        



class AutoFillAction(dd.RowAction):
    label = _("Fill")
    
    def run_from_ui(self,obj,ar,**kw):
        L = list(Invoiceable.get_invoiceables_for(obj.partner,obj.date))
        if len(L) == 0:
            return ar.error(_("No invoiceables found for %s.") % obj.partner)
        def ok():
            for ii in L:
                i = InvoiceItem(voucher=obj,invoiceable=ii,
                    product=ii.get_invoiceable_product())
                i.product_changed(ar)
                i.full_clean()
                i.save()
            kw.update(refresh=True)
            return kw
        msg = _("This will add %d invoice items.") % len(L)
        return ar.confirm(ok, msg, _("Are you sure?"))
    
    
class Invoice(Invoice): # 20130709
    
    auto_fill = AutoFillAction()
    
    class Meta(Invoice.Meta): # 20130709
        #~ app_label = 'sales'
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
    
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
    
    #~ @dd.chooser()
    #~ def enrolment_choices(self,voucher):
        #~ Enrolment = dd.resolve_model('school.Enrolment')
        #~ # print 20130605, voucher.partner.pk
        #~ return Enrolment.objects.filter(pupil__id=voucher.partner.pk).order_by('request_date')
        #~ 
    #~ def enrolment_changed(self,ar):
        #~ if self.enrolment is not None and self.enrolment.course is not None:
            #~ self.product = self.enrolment.course.tariff
        #~ self.product_changed(ar)
        
    def product_changed(self,ar):
        super(InvoiceItem,self).product_changed(ar)
        if self.invoiceable:
            self.title = self.invoiceable.get_invoiceable_title()
        
    
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
    #~ app_label = 'sales'
    master_key = 'invoiceable'
    editable = False
    
#~ sales.ItemsByInvoice.column_names = "enrolment product title description:20x1 discount unit_price qty total_incl total_base total_vat"
    





class InvoiceablesByPartner(dd.VirtualTable):
    #~ app_label = 'sales'
    master = 'contacts.Partner'
    column_names = 'date info'
    
    @classmethod
    def get_data_rows(self,ar):
        rows = []
        mi = ar.master_instance
        if mi is None:
            return rows
        for m in dd.models_by_base(Invoiceable):
            fkw = {m.invoiceable_partner_field:mi}
            for obj in m.objects.filter(**fkw).order_by(m.invoiceable_date_field):
                rows.append((getattr(obj,m.invoiceable_date_field),obj))
        def f(a,b): return cmp(a[0],b[0])
        rows.sort(f)
        return rows
        
    @dd.virtualfield(models.DateField(_("Date")))
    def date(self,row,ar):
        return row[0]
    
    @dd.displayfield(_("Invoiceable"))
    def info(self,row,ar):
        return ar.obj2html(row[1])
    



