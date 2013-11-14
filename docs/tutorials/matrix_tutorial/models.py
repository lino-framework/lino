## Copyright 2013 Luc Saffre
## This file is part of the Lino project.

import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino import dd

contacts = dd.resolve_app('contacts')

class EntryType(dd.BabelNamed):
    class Meta:
        verbose_name = _("Entry Type")
        verbose_name_plural = _("Entry Types")
        
    #~ def after_ui_save(self,ar):
        #~ CompaniesWithEntryTypes.setup_columns()
    
class EntryTypes(dd.Table):
    model = EntryType
    
    
class Entry(dd.UserAuthored):
    
    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")
        
    date = models.DateField(_("Date"))
    entry_type = models.ForeignKey(EntryType)
    subject = models.CharField(_("Subject"),blank=True,max_length=200)
    body = dd.RichTextField(_("Body"),blank=True)
    company = models.ForeignKey('contacts.Company')
    
class Entries(dd.Table):
    model = Entry    
    detail_layout = """
    id user date company
    subject
    body
    """
    insert_layout = """
    user date company
    subject
    """
    parameters = dd.ObservedPeriod(
        entry_type = models.ForeignKey(EntryType,
            blank=True,null=True,
            help_text=_("Show only entries of this type.")),
        company = models.ForeignKey('contacts.Company',
            blank=True,null=True,
            help_text=_("Show only entries of this company.")),
        user = models.ForeignKey(settings.SITE.user_model,
            blank=True,null=True,
            help_text=_("Show only entries by this user.")),
            )
    params_layout = """
    user start_date end_date 
    company entry_type 
    """
    
    @classmethod
    def get_request_queryset(cls,ar):
        qs = super(Entries,cls).get_request_queryset(ar)
        if ar.param_values.end_date:
            qs = qs.filter(date__lte=ar.param_values.end_date)
        if ar.param_values.start_date:
            qs = qs.filter(date__gte=ar.param_values.start_date)
        if ar.param_values.user:
            qs = qs.filter(user=ar.param_values.user)
        if ar.param_values.entry_type:
            qs = qs.filter(entry_type=ar.param_values.entry_type)
        if ar.param_values.company:
            qs = qs.filter(company=ar.param_values.company)
        return qs
    
    @classmethod
    def param_defaults(cls,ar,**kw):
        kw = super(Entries,cls).param_defaults(ar,**kw)
        kw.update(user=ar.get_user())
        return kw
        

    
    
class EntriesByCompany(Entries):
    master_key = 'company'
    
#~ class MyEntries(Entries,dd.ByUser):
    #~ pass
    
    
class CompaniesWithEntryTypes(dd.VentilatingTable,contacts.Companies):
    label = _("Companies with Entry Types")
    hide_zero_rows = True
    parameters = dd.ObservedPeriod()
    params_layout = "start_date end_date"
    editable = False
    auto_fit_column_widths = True
    
    @classmethod
    def param_defaults(cls,ar,**kw):
        kw = super(CompaniesWithEntryTypes,cls).param_defaults(ar,**kw)
        kw.update(end_date=datetime.date.today())
        #~ kw.update(start_date=datetime.date.today())
        return kw
        

    @classmethod
    def get_ventilated_columns(self):
        def w(et):
            # return a getter function for a RequestField on the given EntryType
            def func(fld,obj,ar):
                #~ mi = ar.master_instance
                #~ if mi is None: return None
                pv = dict(start_date=ar.param_values.start_date,end_date=ar.param_values.end_date)
                if et is not None:
                    pv.update(entry_type=et)
                pv.update(company=obj)
                return Entries.request(param_values=pv)
            return func
        for et in EntryType.objects.all():
            yield dd.RequestField(w(et),verbose_name=unicode(et))
        yield dd.RequestField(w(None),verbose_name=_("Total"))
    
   
@dd.receiver(dd.post_save,sender=EntryType)
def my_setup_columns(sender,**kw):
    CompaniesWithEntryTypes.setup_columns()
    
    

@dd.receiver(dd.post_startup)
def my_details_setup(sender,**kw):
    self = sender
    
    self.modules.contacts.Companies.add_detail_tab('entries','matrix_tutorial.EntriesByCompany')


def setup_main_menu(site,ui,profile,m):
    m = m.add_menu("entries",_("Entries"))
    m.add_action(Entries)
    m.add_action(EntryTypes)
    m.add_action(CompaniesWithEntryTypes)
