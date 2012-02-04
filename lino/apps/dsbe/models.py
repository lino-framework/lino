# -*- coding: UTF-8 -*-
## Copyright 2008-2012 Luc Saffre
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
Contains DSBE-specific models and tables that have not yet been 
moved into a separate module because they are really very DSBE specific.

See also :doc:`/dsbe/models`.
"""

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime

from django.db import models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode 
from django.utils.functional import lazy

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation


#~ from lino import reports
from lino import dd
#~ from lino import layouts
from lino.utils import perms
#~ from lino.utils import printable
from lino import mixins
#~ from lino import actions
#~ from lino import fields
from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
#~ from lino.modlib.links import models as links
from lino.modlib.uploads import models as uploads
from lino.modlib.cal import models as cal
from lino.utils.choicelists import HowWell, Gender
from lino.utils.choicelists import ChoiceList
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
from lino.models import get_site_config
from lino.tools import get_field
from lino.tools import resolve_field
from lino.tools import range_filter
from lino.utils.babel import DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils.babel import language_choices
#~ from lino.utils.babel import add_babel_field, DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils import babel 
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
from lino.tools import obj2str

from lino.modlib.countries.models import CountryCity
from lino.modlib.cal.models import DurationUnit, update_auto_task
from lino.modlib.contacts.models import Contact
from lino.tools import resolve_model, UnresolvedModel

#~ # not used here, but these modules are required in INSTALLED_APPS, 
#~ # and other code may import them using 
#~ # ``from lino.apps.dsbe.models import Property``

#~ from lino.modlib.properties.models import Property
#~ # from lino.modlib.notes.models import NoteType
#~ from lino.modlib.countries.models import Country, City

if settings.LINO.user_model:
    User = resolve_model(settings.LINO.user_model,strict=True)


def is_valid_niss(national_id):
    try:
        niss_validator(national_id)
        return True
    except ValidationError:
        return False
        
def niss_validator(national_id):
    """
    Checks whether the specified `national_id` is a valid 
    Belgian NISS (No. d'identification de sécurité sociale).
    """
    if not national_id:
        return
    if len(national_id) != 13:
        raise ValidationError(u'Invalid Belgian NISS %r (length)' % national_id)
    xtest = national_id[:6] + national_id[7:10]
    if national_id[6] == "=":
        xtest = "2" + xtest
    try:
        xtest = int(xtest)
    except ValueError:
        raise ValidationError(u'Invalid Belgian NISS %r (value)' % national_id)
    xtest = abs((xtest-97*(int(xtest/97)))-97)
    if xtest == 0:
        xtest = 97
    if xtest != int(national_id[11:13]):
        raise ValidationError("Invalid Belgian NISS %r (checkdigit)" 
            % national_id)


class CefLevel(ChoiceList):
    """
    Levels of the Common European Framework (CEF).
    
    | http://www.coe.int/t/dg4/linguistic/CADRE_EN.asp
    | http://www.coe.int/t/dg4/linguistic/Source/ManualRevision-proofread-FINAL_en.pdf
    | http://www.telc.net/en/what-telc-offers/cef-levels/a2/
    
    """
    label = _("CEF level")
    
    @classmethod
    def display_text(cls,bc):
        def fn(bc):
            return u"%s (%s)" % (bc.value,unicode(bc))
        return lazy(fn,unicode)(bc)
        #~ return u"%s (%s)" % (bc.value,unicode(bc))
    
add = CefLevel.add_item
add('A1', _("basic language skills"))
add('A2', _("basic language skills"))
add('A2+', _("basic language skills"))
add('B1', _("independent use of language"))
add('B2', _("independent use of language"))
add('B2+', _("independent use of language"))
add('C1', _("proficient use of language"))
add('C2', _("proficient use of language"))
add('C2+', _("proficient use of language"))



CIVIL_STATE_CHOICES = [
  ('1', _("single")   ),
  ('2', _("married")  ),
  ('3', _("divorced") ),
  ('4', _("widowed")  ),
  ('5', _("separated")  ), # Getrennt von Tisch und Bett / 
]


# http://en.wikipedia.org/wiki/European_driving_licence



class ResidenceType(ChoiceList):
    """
    Types of registries for the Belgian residence.
    
    """
    label = _("Residence type")
    
add = ResidenceType.add_item
add('1', _("Registry of citizens"))
add('2', _("Registry of foreigners"))
add('3', _("Waiting for registry"))

#~ RESIDENCE_TYPE_CHOICES = (
  #~ (1  , _("Registry of citizens")   ), # Bevölkerungsregister registre de la population
  #~ (2  , _("Registry of foreigners") ), # Fremdenregister        Registre des étrangers      vreemdelingenregister 
  #~ (3  , _("Waiting for registry")   ), # Warteregister
#~ )

class BeIdCardType(ChoiceList):
    """
    List of Belgian Identification Card Types.
    
    """
    label = _("eID card type")
    
add = BeIdCardType.add_item
add('1',_("Belgian citizen")) 
# ,de=u"Belgischer Staatsbürger",fr=u"Citoyen belge"),
add('6', _("Kids card (< 12 year)")) 
#,de=u"Kind unter 12 Jahren"),
add('8', _("Habilitation")) 
#,fr=u"Habilitation",nl=u"Machtiging")
add('11', _("Foreigner card A"))
        #~ nl=u"Bewijs van inschrijving in het vreemdelingenregister - Tijdelijk verblijf",
        #~ fr=u"Certificat d'inscription au registre des étrangers - Séjour temporaire",
        #~ de=u"Ausländerkarte A Bescheinigung der Eintragung im Ausländerregister - Vorübergehender Aufenthalt",
add('12', _("Foreigner card B"))
        #~ nl=u"Bewijs van inschrijving in het vreemdelingenregister",
        #~ fr=u"Certificat d'inscription au registre des étrangers",
        #~ de=u"Ausländerkarte B (Bescheinigung der Eintragung im Ausländerregister)",
add('13', _("Foreigner card C"))
        #~ nl=u"Identiteitskaart voor vreemdeling",
        #~ fr=u"Carte d'identité d'étranger",
        #~ de=u"C (Personalausweis für Ausländer)",
add('14', _("Foreigner card D"))
        #~ nl=u"EG - langdurig ingezetene",
        #~ fr=u"Résident de longue durée - CE",
        #~ de=u"Daueraufenthalt - EG",
add('15', _("Foreigner card E"))
        #~ nl=u"Verklaring van inschrijving",
        #~ fr=u"Attestation d’enregistrement",
        #~ de=u"Anmeldebescheinigung",
add('16', _("Foreigner card E+"))
add('17', _("Foreigner card F"))
        #~ nl=u"Verblijfskaart van een familielid van een burger van de Unie",
        #~ fr=u"Carte de séjour de membre de la famille d’un citoyen de l’Union",
        #~ de=u"Aufenthaltskarte für Familienangehörige eines Unionsbürgers",
add('18', _("Foreigner card F+"))

#~ BEID_CARD_TYPES = {
  #~ '1' : dict(en=u"Belgian citizen",de=u"Belgischer Staatsbürger",fr=u"Citoyen belge"),
  #~ '6' : dict(en=u"Kids card (< 12 year)",de=u"Kind unter 12 Jahren"),
  #~ '8' : dict(en=u"Habilitation",fr=u"Habilitation",nl=u"Machtiging"),
  #~ '11' : dict(
        #~ en=u"Foreigner card type A",
        #~ nl=u"Bewijs van inschrijving in het vreemdelingenregister - Tijdelijk verblijf",
        #~ fr=u"Certificat d'inscription au registre des étrangers - Séjour temporaire",
        #~ de=u"Bescheinigung der Eintragung im Ausländerregister - Vorübergehender Aufenthalt",
      #~ ),
  #~ '12' : dict(
        #~ en=u"Foreigner card type B",
        #~ nl=u"Bewijs van inschrijving in het vreemdelingenregister",
        #~ fr=u"Certificat d'inscription au registre des étrangers",
        #~ de=u"Bescheinigung der Eintragung im Ausländerregister",
      #~ ),
  #~ '13' : dict(
        #~ en=u"Foreigner card type C",
        #~ nl=u"Identiteitskaart voor vreemdeling",
        #~ fr=u"Carte d'identité d'étranger",
        #~ de=u"Personalausweis für Ausländer",
      #~ ),
  #~ '14' : dict(
        #~ en=u"Foreigner card type D",
        #~ nl=u"EG - langdurig ingezetene",
        #~ fr=u"Résident de longue durée - CE",
        #~ de=u"Daueraufenthalt - EG",
      #~ ),
  #~ '15' : dict(
        #~ en=u"Foreigner card type E",
        #~ nl=u"Verklaring van inschrijving",
        #~ fr=u"Attestation d’enregistrement",
        #~ de=u"Anmeldebescheinigung",
      #~ ),
  #~ '16' : dict(
        #~ en=u"Foreigner card type E+",
      #~ ),
  #~ '17' : dict(
        #~ en=u"Foreigner card type F",
        #~ nl=u"Verblijfskaart van een familielid van een burger van de Unie",
        #~ fr=u"Carte de séjour de membre de la famille d’un citoyen de l’Union",
        #~ de=u"Aufenthaltskarte für Familienangehörige eines Unionsbürgers",
      #~ ),
  #~ '18' : dict(
        #~ en=u"Foreigner card type F+",
      #~ ),
#~ }



class Partner(mixins.DiffingMixin,models.Model):
#~ class Partner(mixins.DiffingMixin,contacts.Contact):
    """
    """
    
    class Meta:
        abstract = True
        app_label = 'contacts'
  
    #~ id = models.AutoField(primary_key=True,verbose_name=_("Partner #"))
    #~ id = models.CharField(max_length=10,primary_key=True,verbose_name=_("ID"))
    
    is_active = models.BooleanField(
        verbose_name=_("is active"),default=True)
    "Only active Persons may be used when creating new operations."
    
    newcomer = models.BooleanField(
        verbose_name=_("newcomer"),default=False)
    """Means that there's no responsible user for this partner yet. 
    New partners may not be used when creating new operations."""
    
    is_deprecated = models.BooleanField(
        verbose_name=_("deprecated"),default=False)
    """Means that data of this partner may be obsolete because 
    there were no confirmations recently. 
    Deprecated partners may not be used when creating new operations."""
    
    activity = models.ForeignKey("dsbe.Activity",
        blank=True,null=True)
    "Pointer to :class:`dsbe.Activity`. May be empty."
    
    bank_account1 = models.CharField(max_length=40,
        blank=True,# null=True,
        verbose_name=_("Bank account 1"))
        
    bank_account2 = models.CharField(max_length=40,
        blank=True,# null=True,
        verbose_name=_("Bank account 2"))
        
    def disable_delete(self,request):
        if settings.TIM2LINO_IS_IMPORTED_PARTNER(self):
            return _("Cannot delete companies and persons imported from TIM")
          

    
class Person(Partner,contacts.PersonMixin,contacts.Contact,contacts.Born,Printable):
    """
    Represents a physical person.
    
    """
    
    class Meta(contacts.PersonMixin.Meta):
        app_label = 'contacts'
        verbose_name = _("Person") # :doc:`/tickets/14`
        verbose_name_plural = _("Persons") # :doc:`/tickets/14`
        
    #~ first_name = models.CharField(max_length=200,blank=True,verbose_name=_('First name'))
    #~ last_name = models.CharField(max_length=200,blank=True,verbose_name=_('Last name'))
    #~ title = models.CharField(max_length=200,blank=True,verbose_name=_('Title'))
        
    def get_queryset(self):
        return self.model.objects.select_related('country','city','coach1','coach2','nationality')
        
    #~ def full_clean(self,*args,**kw):
        #~ l = filter(lambda x:x,[self.last_name,self.first_name,self.title])
        #~ self.name = " ".join(l)
        #~ super(Person,self).full_clean(*args,**kw)
        
    #~ def clean(self):
        #~ l = filter(lambda x:x,[self.last_name,self.first_name,self.title])
        #~ self.name = " ".join(l)
        #~ super(Person,self).clean()
        
    remarks2 = models.TextField(_("Remarks (Social Office)"),blank=True) # ,null=True)
    gesdos_id = models.CharField(max_length=40,blank=True,
        #null=True,
        verbose_name=_("Gesdos ID"))
        
    is_cpas = models.BooleanField(verbose_name=_("receives social help"))
    is_senior = models.BooleanField(verbose_name=_("is senior"))
    #~ is_minor = models.BooleanField(verbose_name=_("is minor"))
    group = models.ForeignKey("dsbe.PersonGroup",blank=True,null=True,
        verbose_name=_("Integration phase"))
    #~ is_dsbe = models.BooleanField(verbose_name=_("is coached"),default=False)
    #~ "Indicates whether this Person is coached."
    
    coached_from = models.DateField(
        blank=True,null=True,
        verbose_name=_("Coached from"))
    coached_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("until"))
    
    coach1 = models.ForeignKey(settings.LINO.user_model,
        blank=True,null=True,
        verbose_name=_("Coach 1"),related_name='coached1')
    coach2 = models.ForeignKey(settings.LINO.user_model,
        blank=True,null=True,
        verbose_name=_("Coach 2"),related_name='coached2')
        
    birth_place = models.CharField(_("Birth place"),
        max_length=200,
        blank=True,
        #null=True
        )
    birth_country = models.ForeignKey("countries.Country",
        blank=True,null=True,
        verbose_name=_("Birth country"),related_name='by_birth_place')
    civil_state = models.CharField(max_length=1,
        blank=True,# null=True,
        verbose_name=_("Civil state"),
        choices=CIVIL_STATE_CHOICES) 
    national_id = models.CharField(max_length=200,
        blank=True,verbose_name=_("National ID")
        #~ ,validators=[niss_validator]
        )
        
    health_insurance = models.ForeignKey(settings.LINO.company_model,blank=True,null=True,
        verbose_name=_("Health insurance"),related_name='health_insurance_for')
    pharmacy = models.ForeignKey(settings.LINO.company_model,blank=True,null=True,
        verbose_name=_("Pharmacy"),related_name='pharmacy_for')
    
    nationality = models.ForeignKey('countries.Country',
        blank=True,null=True,
        related_name='by_nationality',
        verbose_name=_("Nationality"))
    #~ tim_nr = models.CharField(max_length=10,blank=True,null=True,unique=True,
        #~ verbose_name=_("TIM ID"))
    card_number = models.CharField(max_length=20,
        blank=True,#null=True,
        verbose_name=_("eID card number"))
    card_valid_from = models.DateField(
        blank=True,null=True,
        verbose_name=_("ID card valid from"))
    card_valid_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("until"))
        
    #~ card_type = models.CharField(max_length=20,
        #~ blank=True,# null=True,
        #~ verbose_name=_("eID card type"))
    #~ "The type of the electronic ID card. Imported from TIM."
    
    card_type = BeIdCardType.field(blank=True)
    
    card_issuer = models.CharField(max_length=50,
        blank=True,# null=True,
        verbose_name=_("eID card issuer"))
    "The administration who issued this ID card. Imported from TIM."
    
    eid_panel = dd.FieldSet(_("eID card"),
        "card_number card_valid_from card_valid_until card_issuer card_type:20",
        card_number=_("number"),
        card_valid_from=_("valid from"),
        card_valid_until=_("until"),
        card_issuer=_("issued by"),
        #~ card_type=_("card type"),
        #~ card_type_text=_("eID card type"),
        card_type=_("eID card type"),
        )
    
    noble_condition = models.CharField(max_length=50,
        blank=True,#null=True,
        verbose_name=_("noble condition"))
    "The eventual noble condition of this person. Imported from TIM."
        
    
    #~ residence_type = models.SmallIntegerField(blank=True,null=True,
        #~ verbose_name=_("Residence type"),
        #~ choices=RESIDENCE_TYPE_CHOICES,
        #~ max_length=1,
        #~ )
    residence_type = ResidenceType.field(blank=True) 
        
    in_belgium_since = models.DateField(_("Lives in Belgium since"),
        blank=True,null=True)
    unemployed_since = models.DateField(_("Seeking work since"),blank=True,null=True)
    #~ work_permit_exempt = models.BooleanField(verbose_name=_("Work permit exemption"))
    needs_residence_permit = models.BooleanField(verbose_name=_("Needs residence permit"))
    needs_work_permit = models.BooleanField(verbose_name=_("Needs work permit"))
    #~ work_permit_valid_until = models.DateField(blank=True,null=True,verbose_name=_("Work permit valid until"))
    work_permit_suspended_until = models.DateField(blank=True,null=True,verbose_name=_("suspended until"))
    aid_type = models.ForeignKey("dsbe.AidType",blank=True,null=True)
        #~ verbose_name=_("aid type"))
        
    income_ag    = models.BooleanField(verbose_name=_("unemployment benefit")) # Arbeitslosengeld
    income_wg    = models.BooleanField(verbose_name=_("waiting pay")) # Wartegeld
    income_kg    = models.BooleanField(verbose_name=_("sickness benefit")) # Krankengeld
    income_rente = models.BooleanField(verbose_name=_("retirement pension")) # Rente
    income_misc  = models.BooleanField(verbose_name=_("other incomes")) # Andere Einkommen
    
    is_seeking = models.BooleanField(_("is seeking work"))
    unavailable_until = models.DateField(blank=True,null=True,verbose_name=_("Unavailable until"))
    unavailable_why = models.CharField(max_length=100,
        blank=True,# null=True,
        verbose_name=_("reason"))
    
    obstacles = models.TextField(_("Obstacles"),blank=True,null=True)
    skills = models.TextField(_("Other skills"),blank=True,null=True)
    job_agents = models.CharField(max_length=100,
        blank=True,# null=True,
        verbose_name=_("Job agents"))
    
    #~ job_office_contact = models.ForeignKey("contacts.Contact",
    #~ job_office_contact = models.ForeignKey("links.Link",
    job_office_contact = models.ForeignKey("contacts.Role",
      blank=True,null=True,
      verbose_name=_("Contact person at local job office"),
      related_name='persons_job_office')
      
    @chooser()
    def job_office_contact_choices(cls):
        sc = get_site_config()
        if sc.job_office is not None:
            #~ return sc.job_office.contact_set.all()
            #~ return sc.job_office.rolesbyparent.all()
            return sc.job_office.rolesbycompany.all()
            #~ return links.Link.objects.filter(a=sc.job_office)
        return []

    @classmethod
    def setup_report(model,rpt):
        u"""
        rpt.add_action(DirectPrintAction('auskblatt',_("Auskunftsblatt"),'persons/auskunftsblatt.odt'))
        Zur Zeit scheint es so, dass das Auskunftsblatt eher überflüssig wird.
        """
        rpt.add_action(DirectPrintAction(rpt,'eid',_("eID sheet"),'eid-content'))
        #~ rpt.add_action(DirectPrintAction('cv',_("Curiculum vitae"),'persons/cv.odt'))
        
    def __unicode__(self):
        #~ return u"%s (%s)" % (self.get_full_name(salutation=False),self.pk)
        return u"%s %s (%s)" % (self.last_name.upper(),self.first_name,self.pk)
        
    def get_active_contract(self):
        flt = range_filter(datetime.date.today(),'applies_from','applies_until')
        qs1 = self.isip_contract_set_by_person.filter(flt)
        qs2 = self.jobs_contract_set_by_person.filter(flt)
        if qs1.count() + qs2.count() == 1:
            if qs1.count() == 1: return qs1[0]
            if qs2.count() == 1: return qs2[0]
        
    def data_control(self):
        "Used by :class:`lino.models.DataControlListing`."
        msgs = []
        try:
            niss_validator(self.national_id)
        except ValidationError,e:
            msgs.append(unicode(e))
        return msgs
            
    #~ def clean(self):
        #~ if self.job_office_contact: 
            #~ if self.job_office_contact.b == self:
                #~ raise ValidationError(_("Circular reference"))
        #~ super(Person,self).clean()
        
    #~ def card_type_text(self,request):
        #~ if self.card_type:
            #~ s = babeldict_getitem(BEID_CARD_TYPES,self.card_type)
            #~ if s:
                #~ return s
            #~ return _("Unknown card type %r") % self.card_type
        #~ return _("Not specified") # self.card_type
    #~ card_type_text.return_type = dd.DisplayField(_("eID card type"))
        
    def get_print_language(self,pm):
        "Used by DirectPrintAction"
        return self.language
        
    def save(self,*args,**kw):
        if self.job_office_contact: 
            if self.job_office_contact.person == self:
                raise ValidationError(_("Circular reference"))
        super(Person,self).save(*args,**kw)
        self.save_auto_tasks()
        
    def save_auto_tasks(self):
      
        # These constants must be unique for the whole Lino Site.
        # Keep in sync with auto types defined in lino.mixins.reminders
        CARD_VALID_UNTIL = 1
        UNAVAILABLE_UNTIL = 2
        WORK_PERMIT_SUSPENDED_UNTIL = 4
        COACHED_UNTIL = 4
        
        user = self.coach2 or self.coach1
        if user:
            update_auto_task(
              CARD_VALID_UNTIL,user,
              DurationUnit.months.add_duration(self.card_valid_until,-2),
              _("eID card expires"),
              self)
              #~ alarm_value=2,alarm_unit=DurationUnit.months)
              
            update_auto_task(
              UNAVAILABLE_UNTIL,user,
              DurationUnit.months.add_duration(self.unavailable_until,-1),
              _("becomes available again"),
              self)
              #~ alarm_value=1,alarm_unit=DurationUnit.months)
              
            update_auto_task(
              WORK_PERMIT_SUSPENDED_UNTIL,user,
              DurationUnit.months.add_duration(self.work_permit_suspended_until,-1),
              _("work permit suspension ends"),
              self)
              #~ alarm_value=1,alarm_unit=DurationUnit.months)
              
            update_auto_task(
              COACHED_UNTIL,user,
              DurationUnit.months.add_duration(self.coached_until,-1),
              _("coaching ends"),
              self)
              #~ alarm_value=1,alarm_unit=DurationUnit.months)
          
    #~ def get_auto_task_defaults(self,**kw):
    def update_owned_instance(self,task):
        task.project = self
        
    @classmethod
    def get_reminders(model,ui,user,today,back_until):
        q = Q(coach1__exact=user) | Q(coach2__exact=user)
        
        def find_them(fieldname,today,delta,msg,**linkkw):
            filterkw = { fieldname+'__lte' : today + delta }
            if back_until is not None:
                filterkw.update({ 
                    fieldname+'__gte' : back_until
                })
            for obj in model.objects.filter(q,**filterkw).order_by(fieldname):
                linkkw.update(fmt='detail')
                url = ui.get_detail_url(obj,**linkkw)
                html = '<a href="%s">%s</a>&nbsp;: %s' % (url,unicode(obj),cgi.escape(msg))
                yield ReminderEntry(getattr(obj,fieldname),html)
            
        #~ delay = 30
        #~ for obj in model.objects.filter(q,
              #~ card_valid_until__lte=date+datetime.timedelta(days=delay)).order_by('card_valid_until'):
            #~ yield ReminderEntry(obj,obj.card_valid_until,_("eID card expires in %d days") % delay,fmt='detail',tab=3)
        for o in find_them('card_valid_until', today, datetime.timedelta(days=30),
            _("eID card expires"),tab=0):
            yield o
        for o in find_them('unavailable_until', today, datetime.timedelta(days=30),
            _("becomes available again"),tab=1):
            yield o
        for o in find_them('work_permit_suspended_until', today, datetime.timedelta(days=30),
              _("work permit suspension ends"),tab=1):
            yield o
        for o in find_them('coached_until', today, datetime.timedelta(days=30),
            _("coaching ends"),tab=1):
            yield o
        
    @dd.virtualfield(dd.HtmlBox())
    def image(self,request):
        url = self.get_image_url(request)
        #~ s = '<img src="%s" width="100%%" onclick="window.open(\'%s\')"/>' % (url,url)
        s = '<img src="%s" width="100%%"/>' % url
        s = '<a href="%s" target="_blank">%s</a>' % (url,s)
        return s
        #~ return '<img src="%s" width="120px"/>' % self.get_image_url()
    #~ image.return_type = dd.HtmlBox()

    def get_image_parts(self):
        if self.card_number:
            return ("beid",self.card_number+".jpg")
        return ("pictures","contacts.Person.jpg")
        
    def get_image_url(self,request):
        #~ return settings.MEDIA_URL + "/".join(self.get_image_parts())
        return request.ui.media_url(*self.get_image_parts())
        
    def get_image_path(self):
        return os.path.join(settings.MEDIA_ROOT,*self.get_image_parts())
        
    def get_skills_set(self):
        return self.personproperty_set.filter(
          group=settings.LINO.site_config.propgroup_skills)
    skills_set = property(get_skills_set)
    
    def properties_list(self,*prop_ids):
        """
        Yields a list of the :class:`PersonProperty` 
        properties of this person in the specified order.
        If this person has no entry for a 
        requested :class:`Property`, it is simply skipped.
        Used in notes/Note/cv.odt"""
        for pk in prop_ids:
            try:
                yield self.personproperty_set.get(property__id=pk)
            except PersonProperty.DoesNotExist,e:
                pass
        
    def unused_get_property(self,prop_id):
        """used in notes/Note/cv.odt"""
        return self.personproperty_set.get(property__id=prop_id)
        #~ return PersonProperty.objects.get(property_id=prop_id,person=self)
        
        
            
    def overview(self,request):
        def qsfmt(qs):
            s = qs.model._meta.verbose_name_plural + ': '
            if qs.count():
                s += ', '.join([unicode(lk) for lk in qs])
            else:
                s += '<b>%s</b>' % force_unicode(_("not filled in"))
            return force_unicode(s)
        
        lines = []
        #~ lines.append('<div>')
        lines.append(qsfmt(self.languageknowledge_set.all()))
        lines.append(qsfmt(self.study_set.all()))
        lines.append(qsfmt(self.contract_set.all()))
        #~ from django.utils.translation import string_concat
        #~ lines.append('</div>')
        return '<br/>'.join(lines)
    overview.return_type = dd.HtmlBox(_("Overview"))
    
    @dd.displayfield(_("Residence permit"))
    def residence_permit(self,rr):
        kv = dict(type=settings.LINO.site_config.residence_permit_upload_type)
        r = rr.spawn_request(uploads.UploadsByOwner,
              master_instance=self,
              known_values=kv)
        return rr.renderer.quick_upload_buttons(r)
        #~ rrr = uploads.UploadsByPerson().request(rr.ui,master_instance=self,known_values=kv)
        #~ return rr.ui.quick_upload_buttons(rrr)
    #~ residence_permit.return_type = dd.DisplayField(_("Residence permit"))
    
    @dd.displayfield(_("Work permit"))
    def work_permit(self,rr):
        kv = dict(type=settings.LINO.site_config.work_permit_upload_type)
        r = rr.spawn_request(uploads.UploadsByOwner,
              master_instance=self,
              known_values=kv)
        return rr.renderer.quick_upload_buttons(r)
    #~ work_permit.return_type = dd.DisplayField(_("Work permit"))
    
    @dd.displayfield(_("driving licence"))
    #~ @dd.virtualfield(dd.DisplayField(_("driving licence")))
    def driving_licence(self,rr):
        kv = dict(type=settings.LINO.site_config.driving_licence_upload_type)
        r = rr.spawn_request(uploads.UploadsByOwner,
              master_instance=self,known_values=kv)
        return rr.renderer.quick_upload_buttons(r)
    #~ driving_licence.return_type = dd.DisplayField(_("driving licence"))
    
    @dd.displayfield(_("BCSS Identify Person"))
    def bcss_identify_person(self,rr):
        r = rr.spawn_request(
              settings.LINO.modules.bcss.IdentifyRequestsByPerson,
              master_instance=self)
        return rr.renderer.quick_add_buttons(r)

class Contacts(contacts.Contacts):
    imported_fields = []
    
    @classmethod
    def disabled_fields(self,obj,request):
        if settings.TIM2LINO_IS_IMPORTED_PARTNER(obj):
            return self.imported_fields
        return []
        
    @classmethod
    def disable_delete(self,obj,request):
        if settings.TIM2LINO_IS_IMPORTED_PARTNER(obj):
            return _("Cannot delete contacts imported from TIM")
        return super(Contacts,self).disable_delete(obj,request)
        
    @classmethod
    def do_setup(self):
        super(contacts.Contacts,self).do_setup()
        self.imported_fields = dd.fields_list(contacts.Contact,
          '''name remarks region 
          zip_code city country 
          street_prefix street street_no street_box 
          addr2
          language 
          phone fax email url
          is_person is_company
          ''')
        
class AllContacts(contacts.AllContacts,Contacts):
    pass

class Company(Partner,contacts.Contact,contacts.CompanyMixin):
  
    """
    Inner class Meta is necessary because of :doc:`/tickets/14`.
    """
    
    class Meta(contacts.CompanyMixin.Meta):
    #~ class Meta:
        app_label = 'contacts'
        #~ verbose_name = _("Company")
        #~ verbose_name_plural = _("Companies")
        
    #~ vat_id = models.CharField(max_length=200,blank=True)
    #~ type = models.ForeignKey('contacts.CompanyType',blank=True,null=True,verbose_name=_("Company type"))
    prefix = models.CharField(max_length=200,blank=True) 
    # todo: remove hourly_rate after data migration. this is now in Job
    hourly_rate = dd.PriceField(_("hourly rate"),blank=True,null=True)
    #~ is_courseprovider = mti.EnableChild('dsbe.CourseProvider',verbose_name=_("Course provider"))
    
    #~ def disabled_fields(self,request):
        #~ if settings.TIM2LINO_IS_IMPORTED_PARTNER(self):
            #~ return settings.LINO.COMPANY_TIM_FIELDS
        #~ return []
    
  
    
#~ class Companies(reports.Report):
#~ class Companies(contacts.Contacts):
class Companies(Contacts):
    #~ hide_details = [Contact]
    model = settings.LINO.company_model
    order_by = ["name"]
    #~ app_label = 'contacts'
    #~ column_names = ''
    
    @classmethod
    def do_setup(cls):
        super(Companies,cls).do_setup()
        cls.imported_fields = dd.fields_list(cls.model,
            '''name remarks
            zip_code city country street street_no street_box 
            language vat_id
            phone fax email 
            bank_account1 bank_account2 activity''')

#~ class AllPersons(contacts.Persons):
class AllPersons(Contacts):
    #~ hide_details = [Contact]
    #~ model = 'contacts.Person'
    model = settings.LINO.person_model
    order_by = "last_name first_name id".split()
    can_view = perms.is_authenticated
    #~ column_names = "name_column national_id gsm street street_no street_box city age email phone id bank_account1 aid_type coach1 language *"
    #~ column_names = "name_column:20 national_id:10 gsm:10 address_column age:10 email phone:10 id bank_account1 aid_type coach1 language:10 *"
    column_names = "name_column:20 national_id:10 gsm:10 address_column age:10 email phone:10 id bank_account1 aid_type coach1 language:10"
    #~ app_label = 'contacts'
    #~ default_params = dict(is_active=True)
    #~ extra = dict(
      #~ select=dict(sort_name='lower(last_name||first_name)'),
      #~ order_by=['sort_name'])
    #~ order_by = None # clear the default value from contacts.Persons.order_by since we use extra order_by
    
    
    @classmethod
    def init_label(self):
        return string_concat(
          self.model._meta.verbose_name_plural,' ',_("(all)"))
    
    @classmethod
    def do_setup(cls):
        #~ cls.PERSON_TIM_FIELDS = dd.fields_list(cls,
        super(AllPersons,cls).do_setup()
        cls.imported_fields = dd.fields_list(cls.model,
          '''name first_name last_name title remarks remarks2
          zip_code city country street street_no street_box 
          birth_date gender birth_place coach1 language 
          phone fax email 
          card_type card_number card_valid_from card_valid_until
          noble_condition card_issuer
          national_id health_insurance pharmacy 
          bank_account1 bank_account2 
          gesdos_id activity 
          is_cpas is_senior is_active newcomer is_deprecated nationality''')

    #~ @classmethod
    #~ def disabled_fields(self,request):
        #~ if settings.TIM2LINO_IS_IMPORTED_PARTNER(self):
            #~ # return settings.LINO.PERSON_TIM_FIELDS
            #~ return self.__class__.PERSON_TIM_FIELDS
        #~ return []
        
class Persons(AllPersons):
    """
    All Persons except newcomers and inactive persons.
    """
    #~ app_label = 'contacts'
    #~ use_as_default_report = False 
    known_values = dict(is_active=True,newcomer=False)
    #~ filter = dict(is_active=True,newcomer=False)
    #~ label = Person.Meta.verbose_name_plural + ' ' + _("(unfiltered)")
    
    @classmethod
    def init_label(self):
        return self.model._meta.verbose_name_plural

Person._lino_choices_table = Persons

    
class PersonsByNationality(AllPersons):
    #~ app_label = 'contacts'
    master_key = 'nationality'
    order_by = "city name".split()
    column_names = "city street street_no street_box addr2 name country language *"
    


def only_coached_persons(qs,*args,**kw):
    return qs.filter(only_coached_persons_filter(*args,**kw))
    

def only_coached_persons_filter(today):
    """
    coached_from and coached_until
    """
    #~ period_until = period_until or period_from
    # Person with both fields empty is not considered coached:
    q1 = Q(coached_until__isnull=False) | Q(coached_from__isnull=False)
    return Q(q1,range_filter(today,'coached_from','coached_until'))
    
  
def only_my_persons(qs,user):
    return qs.filter(Q(coach1__exact=user) | Q(coach2__exact=user))

class PersonsByCoach1(Persons):
    master_key = 'coach1'
    label = _("Primary clients by coach")
    
    @classmethod
    def get_title(self,rr):
        return _("Primary clients of %s") % rr.master_instance
        
    @classmethod
    def get_request_queryset(self,rr):
        #~ rr.master_instance = rr.get_user()
        qs = super(PersonsByCoach1,self).get_request_queryset(rr)
        #~ only_my_persons(qs,rr.get_user())
        qs = only_coached_persons(qs,datetime.date.today())
        #~ qs = qs.filter()
        #~ print 20111118, 'get_request_queryset', rr.user, qs.count()
        return qs


class MyPersons(Persons):
    """
    Show only persons attended 
    by the requesting user (or another user, 
    specified via :attr:`lino.ui.requests.URL_PARAMS_SUBST_USER`),
    either as primary or as secondary attendant.
    """
    #~ app_label = 'contacts'
    use_as_default_report = False
    label = _("My clients")
    #~ order_by = ['last_name','first_name']
    #~ column_names = "name_column:20 coached_from coached_until national_id:10 gsm:10 address_column age:10 email phone:10 id bank_account1 aid_type coach1 language:10 *"
    column_names = "name_column:20 applies_from applies_until national_id:10 gsm:10 address_column age:10 email phone:10 id bank_account1 aid_type coach1 language:10"
    
    @classmethod
    def get_title(self,rr):
        return _("Clients of %s") % rr.get_user()
        
    @classmethod
    def get_request_queryset(self,rr):
        qs = super(MyPersons,self).get_request_queryset(rr)
        qs = only_coached_persons(only_my_persons(qs,rr.get_user()),datetime.date.today())
        #~ print 20111118, 'get_request_queryset', rr.user, qs.count()
        return qs
        #~ today = datetime.date.today()
        #~ Q = models.Q
        #~ q1 = Q(coach1__exact=rr.user) | Q(coach2__exact=rr.user)
        #~ q2 = Q(coached_from__isnull=False) | Q(coached_until__isnull=False,coached_until__gte=today)
        #~ return qs.filter(q1,q2)
        
    #~ @dd.virtualfield('jobs.Contract.applies_from')
    @dd.virtualfield(models.DateField(_("Contract starts")))
    def applies_from(self,obj,ar):
        c = obj.get_active_contract()
        if c is not None:
            return c.applies_from
            
    #~ @dd.virtualfield('jobs.Contract.applies_until')
    @dd.virtualfield(models.DateField(_("Contract ends")))
    def applies_until(self,obj,ar):
        c = obj.get_active_contract()
        if c is not None:
            return c.applies_until

class MyPersonsByGroup(MyPersons):
    master_key = 'group'
    
    @classmethod
    def get_title(self,rr):
        return _("%(phase)s clients of %(user)s") % dict(
          phase=rr.master_instance, user=rr.get_user())
    
class MyActivePersons(MyPersons):
  
    @classmethod
    def get_title(self,rr):
        return _("Active clients of %s") % rr.get_user()
        
    @classmethod
    def get_request_queryset(self,rr):
        qs = super(MyActivePersons,self).get_request_queryset(rr)
        qs = qs.filter(group__active=True)
        return qs
  

#~ if True: # dd.is_installed('dsbe'):

from lino.tools import models_by_abc


  
#~ class InvalidClients(Persons):
class ClientsTest(Persons):
    """
    Table of persons whose data seems unlogical or inconsistent.
    """
    label = _("Data Test Clients")
    parameters = dict(
      user = models.ForeignKey(User,blank=True,verbose_name=_("Coached by")),
      today = models.DateField(_("only active on"),blank=True,default=datetime.date.today),
      invalid_niss = models.BooleanField(_("Check NISS validity"),default=True),
      overlapping_contracts = models.BooleanField(_("Check for overlapping contracts"),default=True),
      #~ coached_period = models.BooleanField(_("Check coaching period"),default=True),
      #~ only_my_persons = models.BooleanField(_("Only my persons"),default=True),
    )
    params_template = """overlapping_contracts invalid_niss user today"""
    #~ params_panel_hidden = False
    column_names = "name_column error_message national_id id"
    
    @classmethod
    def get_data_rows(self,ar):
        """
        We only want the users who actually have at least one client.
        We store the corresponding request in the user object 
        under the name `my_persons`.
        """
        from lino.modlib.isip.models import OverlappingContractsTest
        #~ qs = Person.objects.all()
        qs = self.get_request_queryset(ar)
        
        if ar.param_values.user:
            qs = only_my_persons(qs,ar.param_values.user)
        
        if ar.param_values.today:
            qs = only_coached_persons(qs,ar.param_values.today)
            
        logger.info("Building ClientsTest data rows...")
        #~ for p in qs.order_by('name'):
        for person in qs:
            messages = []
            if ar.param_values.overlapping_contracts:
                messages += OverlappingContractsTest(person).check_all()
              
            if ar.param_values.invalid_niss:
                try:
                    niss_validator(person.national_id)
                except ValidationError,e:
                    messages += e.messages
          
            if messages:
                #~ person.error_message = ';<br/>'.join([cgi.escape(m) for m in messages])
                person.error_message = ';\n'.join(messages)
                #~ logger.info("%s : %s", p, p.error_message)
                yield person
        logger.info("Building ClientsTest data rows: done")
                
        
    @dd.displayfield(_('Error message'))
    def error_message(self,obj,ar):
        #~ return obj.error_message.replace('\n','<br/>')
        return obj.error_message
        
    
#~ class OverviewClientsByUser(dd.VirtualTable):
class UsersWithClients(dd.VirtualTable):
    """
    New implementation of persons_by_user
    A customized overview report.
    """
    #~ label = _("Overview Clients By User")
    label = _("Users with their Clients")
    #~ column_defaults = dict(width=8)
    
    #~ @classmethod
    #~ def before_ui_handle(self,ui):
        #~ """
        #~ Builds columns dynamically from the :class:`PersonGroup` database table.
        #~ Called when kernel setup is done, 
        #~ before the UI handle is being instantiated.
        #~ """
        #~ self.column_names = 'user:10'
        #~ for pg in PersonGroup.objects.filter(ref_name__isnull=False).order_by('ref_name'):
            #~ def w(pg):
                #~ def func(self,obj,ar):
                    #~ return MyPersonsByGroup.request(
                      #~ ar.ui,master_instance=pg,subst_user=obj)
                #~ return func
            #~ vf = dd.RequestField(w(pg),verbose_name=pg.name)
            #~ self.add_virtual_field('G'+pg.ref_name,vf)
            #~ self.column_names += ' ' + vf.name 
            
        #~ self.column_names += ' primary_clients active_clients row_total'
        #~ super(OverviewClientsByUser,self).before_ui_handle(ui)
        
    @classmethod
    def setup_columns(self):
        """
        Builds columns dynamically from the :class:`PersonGroup` database table.
        Called when kernel setup is done, 
        before the UI handle is being instantiated.
        """
        self.column_names = 'user:10'
        try:
            for pg in PersonGroup.objects.filter(ref_name__isnull=False).order_by('ref_name'):
                def w(pg):
                    def func(self,obj,ar):
                        return MyPersonsByGroup.request(
                          ar.ui,master_instance=pg,subst_user=obj)
                    return func
                vf = dd.RequestField(w(pg),verbose_name=pg.name)
                self.add_virtual_field('G'+pg.ref_name,vf)
                self.column_names += ' ' + vf.name 
        except DatabaseError:
            # happens during `make appdocs`
            pass
            
        self.column_names += ' primary_clients active_clients row_total'
    
    @classmethod
    def get_data_rows(self,ar):
        """
        We only want the users who actually have at least one client.
        We store the corresponding request in the user object 
        under the name `my_persons`.
        """
        for user in User.objects.filter(
            Q(username=ar.get_user().username) | Q(is_spis=True)
          ).order_by('username'):
            r = MyPersons.request(ar.ui,subst_user=user)
            if r.get_total_count():
            #~ if len(r.data_iterator):
                user.my_persons = r
                yield user
                
    @dd.virtualfield('contacts.Person.coach1')
    def user(self,obj,ar):
        return obj
        
    @dd.requestfield(_("Total"))
    def row_total(self,obj,ar):
        return obj.my_persons
        
    @dd.requestfield(_("Primary clients"))
    def primary_clients(self,obj,ar):
        return PersonsByCoach1.request(ar.ui,master_instance=obj)
        
    @dd.requestfield(_("Active clients"))
    def active_clients(self,obj,ar):
        return MyActivePersons.request(ar.ui,subst_user=obj)
        
        

def persons_by_user(ui,requesting_user):
    """
    Returns a summary table "Number of clients by user and integration phase"
    """
    assert requesting_user is not None
    renderer = ui.ext_renderer
    
    #~ from django.utils.translation import ugettext as _
    #~ from lino.modlib.users.models import User  
    #~ User = resolve_model('users.User')
    User = resolve_model(settings.LINO.user_model)
    #~ User = settings.LINO.get_user_model()
    #~ from lino.apps.dsbe.models import PersonGroup,Person,only_coached_persons,only_my_persons
    headers = [cgi.escape(_("User"))]
    totals = [cgi.escape(_("Total"))]
    sums = []
    pg2col = {}
    phases = [pg for pg in PersonGroup.objects.order_by('ref_name')]
    for pg in phases:
        headers.append('<font size="2">%s</font>' % cgi.escape(pg.name))
        sums.append('')
        totals.append(0)
        pg2col[pg.pk] = len(headers) - 1
    #~ phases.append(None)
    headers.append(cgi.escape(_("Primary clients")))
    headers.append(cgi.escape(_("Active clients")))
    headers.append(cgi.escape(_("Total")))
    totals.append(0)
    totals.append(0)
    totals.append(0)
        
    rows = [ headers ]
    for user in User.objects.order_by('username'):
        if user == requesting_user or user.is_spis:
            #~ rr = MyPersons.request(ui,user=user)
            #~ kv = dict(user=user)
            rr = MyPersons.request(ui,subst_user=user)
            #~ rr = MyPersons.request(ui,known_values=kv)
            if rr.get_total_count():
            #~ if len(rr.data_iterator):
                totals[-1] += rr.get_total_count()
                row_total = renderer.href_to_request(rr,str(rr.get_total_count()))
                cells = [cgi.escape(unicode(user))] + sums
                for pg in phases:
                    rr = MyPersonsByGroup.request(ui,master_instance=pg,subst_user=user)
                    if rr.get_total_count():
                        totals[pg2col[pg.pk]] += rr.get_total_count()
                        text = str(rr.get_total_count())
                        text = renderer.href_to_request(rr,text)
                        cells[pg2col[pg.pk]] = text
                def yet_another_column(i,rr):
                    totals[i] += rr.get_total_count()
                    text = str(rr.get_total_count())
                    text = renderer.href_to_request(rr,text)
                    cells.append(text)
                yet_another_column(-3,PersonsByCoach1.request(ui,master_instance=user))
                yet_another_column(-2,MyActivePersons.request(ui,subst_user=user))
                cells.append(row_total)
                rows.append(cells)
    rows.append(totals)
        
    s = ''
    for row in rows:
        s += '<tr>'
        s += ''.join(['<td align="center" valign="middle" bgcolor="#eeeeee">%s</td>' % cell for cell in row])
        s += '</tr>'
    s = '<table cellspacing="3px" bgcolor="#ffffff" width="100%%"><tr>%s</tr></table>' % s
    s = '<div class="htmlText">%s</div>' % s
    return s
    
    

#
# PERSON GROUP
#
class PersonGroup(models.Model):
    """Integration Phase (previously "Person Group")
    """
    name = models.CharField(_("Designation"),max_length=200)
    ref_name = models.CharField(_("Reference name"),max_length=20,blank=True)
    active = models.BooleanField(_("Considered active"),default=True)
    #~ text = models.TextField(_("Description"),blank=True,null=True)
    class Meta:
        verbose_name = _("Integration Phase")
        verbose_name_plural = _("Integration Phases")
    def __unicode__(self):
        return self.name

class PersonGroups(dd.Table):
    """List of Integration Phases"""
    model = PersonGroup
    order_by = ["ref_name"]

    
    
    
#
# LanguageKnowledge
#

class LanguageKnowledge(models.Model):
    """Specifies how well a certain Person knows a certain Language.
    Deserves more documentation."""
    class Meta:
        verbose_name = _("language knowledge")
        verbose_name_plural = _("language knowledges")
        
    allow_cascaded_delete = True
    
    #~ person = models.ForeignKey("contacts.Person")
    person = models.ForeignKey(settings.LINO.person_model)
    language = models.ForeignKey("countries.Language",verbose_name=_("Language"))
    #~ language = models.ForeignKey("countries.Language")
    #~ language = fields.LanguageField()
    spoken = HowWell.field(verbose_name=_("spoken"))
    written = HowWell.field(verbose_name=_("written"))
    native = models.BooleanField(verbose_name=_("native language"))
    cef_level = CefLevel.field(blank=True) # ,null=True)
    
    def __unicode__(self):
        if self.language_id is None:
            return ''
        if self.cef_level:
            return u"%s (%s)" % (self.language,self.cef_level)
        if self.spoken > '1' and self.written > '1':
            return _(u"%s (s/w)") % self.language
        elif self.spoken > '1':
            return _(u"%s (s)") % self.language
        elif self.written > '1':
            return _(u"%s (w)") % self.language
        else:
            return unicode(self.language)
      
    
class LanguageKnowledgesByPerson(dd.Table):
    model = LanguageKnowledge
    master_key = 'person'
    #~ label = _("Language knowledge")
    #~ button_label = _("Languages")
    column_names = "language native spoken written cef_level"

# 
# PROPERTIES
# 

from lino.modlib.properties import models as properties

class PersonProperty(properties.PropertyOccurence):
    """A given property defined for a given person. 
    See :mod:`lino.modlib.properties`."""
    
    allow_cascaded_delete = True
    
    class Meta:
        app_label = 'properties'
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
        
    #~ person = models.ForeignKey("contacts.Person")
    person = models.ForeignKey(settings.LINO.person_model)
    remark = models.CharField(max_length=200,
        blank=True,# null=True,
        verbose_name=_("Remark"))
  
class PropsByPerson(dd.Table):
    model = PersonProperty
    master_key = 'person'
    column_names = "property value remark *"
    hidden_columns = frozenset(['group'])
    
    
class PersonPropsByProp(dd.Table):
    model = PersonProperty
    #~ app_label = 'properties'
    master_key = 'property'
    column_names = "person value remark *"
    hidden_columns = frozenset(['group'])
    
#~ class PersonPropsByType(dd.Table):
    #~ model = PersonProperty
    #~ master_key = 'type'
    #~ column_names = "person property value remark *"
    #~ hidden_columns = frozenset(['group'])
    
from django.utils.functional import lazy
    
class ConfiguredPropsByPerson(PropsByPerson):
    """
    Base class for 
    :class`SkillsByPerson`, 
    :class`SoftSkillsByPerson` and
    :class`ObstaclesByPerson`.
    """
    propgroup_config_name = None
    typo_check = False # to avoid warning "ConfiguredPropsByPerson 
                       # defines new attribute(s) propgroup_config_name"
    @classmethod
    def setup_actions(self):
        if self.propgroup_config_name:
            pg = getattr(settings.LINO.site_config,self.propgroup_config_name)
            self.known_values = dict(group=pg)
            if pg is None:
                self.label = _("(Site setting %s is empty)" % self.propgroup_config_name)
            else:
                #~ def f():
                    #~ return babelattr(pg,'name')
                #~ self.label = lazy(f,unicode)()
                self.label = lazy(babelattr,unicode)(pg,'name')
                #~ self.label = babelattr(pg,'name')
        super(PropsByPerson,self).setup_actions()
        
class SkillsByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_skills'
        
class SoftSkillsByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_softskills'
        
class ObstaclesByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_obstacles'
    
    

#
# ACTIVITIY (Berufscode)
#
class Activity(models.Model):
    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
    name = models.CharField(max_length=80)
    lst104 = models.BooleanField(_("Appears in Listing 104"))
    
    def __unicode__(self):
        return unicode(self.name)

class Activities(dd.Table):
    model = Activity
    #~ label = _('Activities')

#~ class ActivitiesByPerson(Activities):
    #~ master_key = 'activity'

#~ class ActivitiesByCompany(Activities):
    #~ master_key = 'activity'
    
#
# EXCLUSION TYPES (Sperrgründe)
#
class ExclusionType(models.Model):
    class Meta:
        verbose_name = _("exclusion type")
        verbose_name_plural = _('exclusion types')
        
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return unicode(self.name)

class ExclusionTypes(dd.Table):
    model = ExclusionType
    #~ label = _('Exclusion Types')
    
#
# EXCLUSIONS (Arbeitslosengeld-Sperrungen)
#
class Exclusion(models.Model):
    class Meta:
        verbose_name = _("exclusion")
        verbose_name_plural = _('exclusions')
        
    #~ person = models.ForeignKey("contacts.Person")
    person = models.ForeignKey(settings.LINO.person_model)
    type = models.ForeignKey("dsbe.ExclusionType",verbose_name=_("Reason"))
    excluded_from = models.DateField(blank=True,null=True,verbose_name=_("from"))
    excluded_until = models.DateField(blank=True,null=True,verbose_name=_("until"))
    remark = models.CharField(max_length=200,blank=True,verbose_name=_("Remark"))
    
    def __unicode__(self):
        s = unicode(self.type)
        if self.excluded_from: s += ' ' +unicode(self.excluded_from)
        if self.excluded_until: s += '-'+unicode(self.excluded_until)
        return s

class Exclusions(dd.Table):
    model = Exclusion
    #~ label = _('Exclusions')
    
class ExclusionsByPerson(Exclusions):
    master_key = 'person'
    column_names = 'excluded_from excluded_until type remark'


#
# COACHING TYPES 
#
#~ class CoachingType(models.Model):
    #~ class Meta:
        #~ verbose_name = _("coaching type")
        #~ verbose_name_plural = _('coaching types')
        
    #~ name = models.CharField(max_length=200)
    
    #~ def __unicode__(self):
        #~ return unicode(self.name)

#~ class CoachingTypes(dd.Table):
    #~ model = CoachingType
    
#
# COACHINGS
#
#~ class Coaching(models.Model):
    #~ class Meta:
        #~ verbose_name = _("coaching")
        #~ verbose_name_plural = _('coachings')
    #~ person = models.ForeignKey("contacts.Person",verbose_name=_("Client"))
    #~ coach = models.ForeignKey("auth.User",verbose_name=_("Coach"))
    #~ type = models.ForeignKey("dsbe.CoachingType",verbose_name=_("Coaching type"))
    #~ remark = models.CharField(max_length=200,blank=False,verbose_name=_("Remark"))
    

#~ class Coachings(dd.Table):
    #~ model = Coaching
    
#~ class CoachingsByPerson(Coachings):
    #~ master_key = 'person'
    #~ column_names = 'coach type remark *'
    #~ label = _('Coaches')

#
# COURSE ENDINGS
#
class CourseEnding(models.Model):
    u"""
    Eine Kursbeendigung ist eine *Art und Weise, wie eine Kursanfrage beendet wurde*.
    Später können wir dann Statistiken machen, wieviele Anfragen auf welche Art und 
    Weise beendet wurden.
    """
    class Meta:
        verbose_name = _("Course Ending")
        verbose_name_plural = _('Course Endings')
        
    name = models.CharField(_("designation"),max_length=200)
    
    def __unicode__(self):
        return unicode(self.name)
        
class CourseEndings(dd.Table):
    model = CourseEnding
    column_names = 'name *'
    order_by = ['name']


#
# AID TYPES
#
class AidType(babel.BabelNamed):
    class Meta:
        verbose_name = _("aid type")
        verbose_name_plural = _('aid types')
        
    #~ name = babel.BabelCharField(_("designation"),max_length=200)
    
    #~ def __unicode__(self):
        #~ return unicode(babel.babelattr(self,'name'))
#~ add_babel_field(AidType,'name')

class AidTypes(dd.Table):
    model = AidType
    column_names = 'name *'



#
# CALENDAR IMPLEMENTATION AND EXTENSION
#

#~ class ComponentMixin(contacts.PartnerDocument):
#~ class ComponentMixin(mixins.ProjectRelated):
  
    #~ class Meta:
        #~ abstract = True
  
    #~ def summary_row(self,ui,rr,**kw):
        #~ html = mixins.ProjectRelated.summary_row(self,ui,rr,**kw)
        # html = contacts.PartnerDocument.summary_row(self,ui,rr,**kw)
        #~ if self.summary:
            #~ html += '&nbsp;: %s' % cgi.escape(force_unicode(self.summary))
            # html += ui.href_to(self,force_unicode(self.summary))
        #~ html += _(" on ") + babel.dtos(self.start_date)
        #~ return html

#~ class Event(cal.Event,ComponentMixin):
    #~ class Meta(cal.Event.Meta):
        #~ app_label = 'cal'

#~ class Task(cal.Task,ComponentMixin):
    #~ class Meta(cal.Task.Meta):
        #~ app_label = 'cal'

#~ class EventsByProject(cal.Events):
    #~ master_key = 'project'
    
#~ class TasksByProject(cal.Tasks):
    #~ master_key = 'project'
    
#~ class EventsByPerson(cal.Events):
    #~ master_key = 'person'
    
#~ class EventsByCompany(cal.Events):
    #~ master_key = 'company'

#~ class TasksByPerson(cal.Tasks):
    #~ master_key = 'person'
    
#~ class TasksByCompany(cal.Tasks):
    #~ master_key = 'company'
    
        

  
#
# LINKS IMPLEMENTATION AND EXTENSION
#
#~ class Link(links.Link,contacts.PartnerDocument):
    #~ class Meta:
        #~ app_label = 'links'

#~ class LinksByPerson(links.LinksByOwnerBase):
    #~ master_key = 'person'
    #~ column_names = "name url user date company *"
    #~ order_by = ["date"]
  
#~ class LinksByCompany(links.LinksByOwnerBase):
    #~ master_key = 'company'
    #~ column_names = "name url user date person *"
    #~ order_by = ["date"]
    

#
# COURSES
#


#~ class CourseProvider(models.Model):
class CourseProvider(Company):
    """
    A CourseProvider is a Company that offers Courses. 
    """
    class Meta:
        app_label = 'dsbe'
    #~ name = models.CharField(max_length=200,
          #~ verbose_name=_("Name"))
    #~ company = models.ForeignKey("contacts.Company",blank=True,null=True,verbose_name=_("Company"))
    

class CourseProviders(Companies):
    """
    List of Companies that have `Company.is_courseprovider` activated.
    """
    #~ hide_details = [Contact]
    #~ use_as_default_report = False
    #~ app_label = 'dsbe'
    label = _("Course providers")
    model = CourseProvider
    #~ known_values = dict(is_courseprovider=True)
    #~ filter = dict(is_courseprovider__exact=True)
    
    #~ def create_instance(self,req,**kw):
        #~ instance = super(CourseProviders,self).create_instance(req,**kw)
        #~ instance.is_courseprovider = True
        #~ return instance
  
class CourseContent(models.Model):
    u"""
    Ein Kursinhalt (z.B. "Französisch", "Deutsch", "Alphabétisation",...)
    """
    
    class Meta:
        verbose_name = _("Course Content")
        verbose_name_plural = _('Course Contents')
        
    name = models.CharField(max_length=200,
          blank=True,# null=True,
          verbose_name=_("Name"))
    u"""
    Bezeichnung des Kursinhalts (nach Konvention des DSBE).
    """
          
    def __unicode__(self):
        return unicode(self.name)
        
  
class CourseOffer(models.Model):
    """
    """
    class Meta:
        verbose_name = _("Course Offer")
        verbose_name_plural = _('Course Offers')
        
    title = models.CharField(max_length=200,
        verbose_name=_("Name"))
    u"""
    Der Titel des Kurses. Maximal 200 Zeichen.
    """
    
    content = models.ForeignKey("dsbe.CourseContent",
        verbose_name=_("Course content"))
    """
    Der Inhalt des Kurses (ein :class:`CourseContent`)
    """
    
    provider = models.ForeignKey(CourseProvider,
        verbose_name=_("Course provider"))
    """
    Der Kursanbieter (eine :class:`Company`)
    """
    
    description = dd.RichTextField(_("Description"),blank=True,format='html')
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title,self.provider)
        
    @chooser()
    def provider_choices(cls):
        return CourseProviders.request().queryset
        
    #~ @classmethod
    #~ def setup_report(model,rpt):
        #~ rpt.add_action(DirectPrintAction('candidates',_("List of candidates"),'candidates'))
        
    def get_print_language(self,pm):
        "Used by DirectPrintAction"
        return DEFAULT_LANGUAGE
        
        
    
class Course(models.Model,mixins.Printable):
    u"""
    Ein konkreter Kurs, der an einem bestimmten Datum beginnt.
    Für jeden Kurs muss ein entsprechendes Angebot existieren, 
    das u.A. den :class:`Kursinhalt <CourseContent>` 
    und :class:`Kursanbieter <CourseProvider>` 
    detailliert. Also selbst für einen einmalig stattfindenden 
    Kurs muss ein Angebot erstellt werden.
    """
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _('Courses')
        
        
    offer = models.ForeignKey("dsbe.CourseOffer")
    
    title = models.CharField(max_length=200,
        blank=True,
        verbose_name=_("Name"))
        
    start_date = models.DateField(_("start date"))
    
    #~ content = models.ForeignKey("dsbe.CourseContent",verbose_name=_("Course content"))
  
    remark = models.CharField(max_length=200,
        blank=True,# null=True,
        verbose_name=_("Remark"))
    u"""
    Bemerkung über diesen konkreten Kurs. Maximal 200 Zeichen.
    """
        
    def __unicode__(self):
        #~ s = u"%s %s (%s)" % (self._meta.verbose_name,self.pk,babel.dtos(self.start_date))
        s = babel.dtos(self.start_date)
        if self.title:
            s += " " + self.title
        if self.offer:
            s += " " + unicode(self.offer)
        return s
  
    @classmethod
    def setup_report(model,rpt):
        rpt.add_action(DirectPrintAction(rpt,'candidates',_("List of candidates"),'candidates'))
        rpt.add_action(DirectPrintAction(rpt,'participants',_("List of participants"),'participants'))
        
    def get_print_language(self,pm):
        "Used by DirectPrintAction"
        return DEFAULT_LANGUAGE
        
    def participants(self):
        u"""
        Liste von :class:`CourseRequest`-Instanzen, 
        die in diesem Kurs eingetragen sind. 
        """
        return ParticipantsByCourse.request(master_instance=self).data_iterator
        
    def candidates(self):
        u"""
        Liste von :class:`CourseRequest`-Instanzen, 
        die noch in keinem Kurs eingetragen sind, aber für diesen Kurs in Frage 
        kommen. 
        """
        return CandidatesByCourse.request(master_instance=self).data_iterator
        
        
class CourseRequest(models.Model):
    """
    A Course Request is created when a certain Person expresses her 
    wish to participate in a Course with a certain CourseContent.
    """
    class Meta:
        verbose_name = _("Course Requests")
        verbose_name_plural = _('Course Requests')
        
    #~ person = models.ForeignKey("contacts.Person",
    person = models.ForeignKey(settings.LINO.person_model,
        verbose_name=_("Person"),
        help_text=u"Die Person, die die Anfrage macht.")
    
    offer = models.ForeignKey("dsbe.CourseOffer",blank=True,null=True)
    
    content = models.ForeignKey("dsbe.CourseContent",
        verbose_name=_("Course content"),
        help_text=u"Der gewünschte Kursinhalt (ein Objekt vom Typ :class:`CourseConent`.)")
    
    #~ date_submitted = models.DateField(_("date submitted"),auto_now_add=True)
    date_submitted = models.DateField(_("date submitted"),
        help_text=u"Das Datum, an dem die Anfrage erstellt wurde.")
    
    urgent = models.BooleanField(_("Urgent"),default=False,
        help_text=u"Ankreuzen, wenn der Kurs für die Arbeitssuche benötigt wird.")
    
    #~ """Empty means 'any provider'
    #~ """
    #~ provider = models.ForeignKey(CourseProvider,blank=True,null=True,
        #~ verbose_name=_("Course provider"))
        
    #~ @chooser()
    #~ def provider_choices(cls):
        #~ return CourseProviders.request().queryset
        
    course = models.ForeignKey("dsbe.Course",blank=True,null=True,
        verbose_name=_("Course found"))
    u"""
    Der Kurs, durch den diese Anfrage befriedigt wurde.
    So lange dieses Feld leer ist, gilt die Anfrage als offen.
    """
        
    #~ """
    #~ The person's feedback about how satisfied she was.
    #~ """
    #~ satisfied = StrengthField(verbose_name=_("Satisfied"),blank=True,null=True)
    
    #~ remark = models.CharField(max_length=200,
    remark = models.TextField(
        blank=True,null=True,
        verbose_name=_("Remark"))
    u"""
    Bemerkung zu dieser konkreten Kursanfrage oder -teilnahme.
    """
        
    date_ended = models.DateField(blank=True,null=True,verbose_name=_("date ended"))
    u"""
    Datum der effektives Beendigung dieser Kursteilname.
    """
    
    ending = models.ForeignKey("dsbe.CourseEnding",blank=True,null=True,
        verbose_name=_("Ending"))
    u"""
    Die Art der Beendigung 
    (ein Objekt vom Typ :class:`CourseEnding`.)
    Das wird benutzt für spätere Statistiken.
    """
    
    def save(self,*args,**kw):
        if self.offer and self.offer.content:
            self.content = self.offer.content
        super(CourseRequest,self).save(*args,**kw)
        
    @chooser()
    def offer_choices(cls,content):
        if content:
            return CourseOffer.objects.filter(content=content)
        return CourseOffer.objects.all()
        
    
    def on_create(self,req):
        self.date_submitted = datetime.date.today()
    
        
class Courses(dd.Table):
    model = Course
    order_by = ['start_date']
    
class CoursesByOffer(Courses):
    master_key = 'offer'
    column_names = 'start_date * id'

class CourseContents(dd.Table):
    model = CourseContent
    order_by = ['name']

class CourseOffers(dd.Table):
    model = CourseOffer
    
class CourseOffersByProvider(CourseOffers):
    master_key = 'provider'

class CourseRequests(dd.Table):
    model = CourseRequest
    order_by = ['date_submitted']
    active_fields = ['offer']

class CourseRequestsByPerson(CourseRequests):
    master_key = 'person'
    column_names = 'date_submitted:10 content:15 offer:15 course:20 * id'

class RequestsByCourse(CourseRequests):
    master_key = 'course'
  
    @classmethod
    def create_instance(self,req,**kw):
        obj = super(RequestsByCourse,self).create_instance(req,**kw)
        if obj.course is not None:
            obj.content = obj.course.offer.content
        return obj
    
class RegisterCandidate(dd.RowAction):
    """
    Register the given :class:`Candidate` for the given :class:`Course`.
    This action is available on a row of :class:`CandidatesByCourse`.
    """
    label = _("Register")
    name = "register"
    def run(self,rr,elem):
        elem.course = rr.master_instance
        elem.save()
        return rr.ui.success_response(refresh_all=True,
          message=_("%(person)s has been registered to %(course)s") % dict(
              person=elem.person,course=elem.course))

class UnregisterCandidate(dd.RowAction):
    """
    Unregister the given :class:`Candidate` for the given :class:`Course`.
    This action is available on a row of :class:`ParticipantsByCourse`.
    """
    label = _("Unregister")
    name = "unregister"
    def run(self,rr,elem):
        course = elem.course
        elem.course = None
        elem.save()
        return rr.ui.success_response(refresh_all=True,
          message=_("%(person)s has been unregistered from %(course)s") % dict(person=elem.person,course=course))

class ParticipantsByCourse(RequestsByCourse):
    """
    List of participating :class:`Candidates <Candidate>` for the given :class:`Course`.
    """
    label = _("Participants")
    column_names = 'person remark date_ended ending'
    
    @classmethod
    def setup_actions(self):
        self.add_action(UnregisterCandidate())

class CandidatesByCourse(RequestsByCourse):
    """
    List of :class:`Candidates <Candidate>` for the given :class:`Course`
    which are not registiered.
    """
    label = _("Candidates")
    column_names = 'person remark content date_submitted'
    #~ can_add = perms.never
    
    @classmethod
    def setup_actions(self):
        self.add_action(RegisterCandidate())
    
    @classmethod
    def get_request_queryset(self,rr):
        if rr.master_instance is None:
            return []
        return self.model.objects.filter(course__isnull=True,
            content__exact=rr.master_instance.offer.content)
    
    @classmethod
    def create_instance(self,req,**kw):
        """Manually clear the `course` field.
        """
        obj = super(CandidatesByCourse,self).create_instance(req,**kw)
        obj.course = None
        return obj

#
# SEARCH
#
class PersonSearch(mixins.AutoUser,mixins.Printable):
    class Meta:
        verbose_name = _("Person Search")
        verbose_name_plural = _('Person Searches')
        
    title = models.CharField(max_length=200,
        verbose_name=_("Search Title"))
    aged_from = models.IntegerField(_("Aged from"),
        blank=True,null=True)
    aged_to = models.IntegerField(_("Aged to"),
        blank=True,null=True)
    #~ gender = contacts.GenderField()
    gender = Gender.field()

    
    only_my_persons = models.BooleanField(_("Only my persons")) # ,default=True)
    
    coached_by = models.ForeignKey(settings.LINO.user_model,
        verbose_name=_("Coached by"),
        related_name='persons_coached',
        blank=True,null=True)
    period_from = models.DateField(
        blank=True,null=True,
        verbose_name=_("Period from"))
    period_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("until"))
    
    def result(self):
        for p in PersonsBySearch().request(master_instance=self):
            yield p
        
    def __unicode__(self):
        return self._meta.verbose_name + ' "%s"' % (self.title or _("Unnamed"))
        
    #~ def get_print_language(self,pm):
        #~ return DEFAULT_LANGUAGE
        
    @classmethod
    def setup_report(model,rpt):
        rpt.add_action(DirectPrintAction(rpt,'suchliste',_("Print"),'suchliste'))
        
class MySearches(mixins.ByUser):
    model = PersonSearch
    
class WantedLanguageKnowledge(models.Model):
    search = models.ForeignKey(PersonSearch)
    language = models.ForeignKey("countries.Language",verbose_name=_("Language"))
    spoken = HowWell.field(verbose_name=_("spoken"))
    written = HowWell.field(verbose_name=_("written"))

class WantedSkill(properties.PropertyOccurence):
    class Meta:
        app_label = 'properties'
        verbose_name = _("Wanted property")
        verbose_name_plural = _("Wanted properties")
        
    search = models.ForeignKey(PersonSearch)
    
class UnwantedSkill(properties.PropertyOccurence):
    class Meta:
        app_label = 'properties'
        verbose_name = _("Unwanted property")
        verbose_name_plural = _("Unwanted properties")
    search = models.ForeignKey(PersonSearch)
    
    
class LanguageKnowledgesBySearch(dd.Table):
    label = _("Wanted language knowledges")
    master_key = 'search'
    model = WantedLanguageKnowledge

class WantedPropsBySearch(dd.Table):
    label = _("Wanted properties")
    master_key = 'search'
    model = WantedSkill

class UnwantedPropsBySearch(dd.Table):
    label = _("Unwanted properties")
    master_key = 'search'
    model = UnwantedSkill

class PersonSearches(dd.Table):
    model = PersonSearch
    
class PersonsBySearch(dd.Table):
    """
    This is the slave report of a PersonSearch that shows the 
    Persons matching the search criteria. 
    
    It is a slave report without 
    :attr:`master_key <lino.dd.Table.master_key>`,
    which is allowed only because it also overrides
    :meth:`get_request_queryset`
    """
  
    model = Person
    master = PersonSearch
    #~ 20110822 app_label = 'dsbe'
    label = _("Found persons")
    
    can_add = perms.never
    can_change = perms.never
    
    @classmethod
    def get_request_queryset(self,rr):
        """
        Here is the code that builds the query. It can be quite complex.
        See :srcref:`/lino/apps/dsbe/models.py` 
        (search this file for "PersonsBySearch").
        """
        search = rr.master_instance
        if search is None:
            return []
        kw = {}
        qs = self.model.objects.order_by('name')
        today = datetime.date.today()
        if search.gender:
            qs = qs.filter(gender__exact=search.gender)
        if search.aged_from:
            #~ q1 = models.Q(birth_date__isnull=True)
            #~ q2 = models.Q(birth_date__gte=today-datetime.timedelta(days=search.aged_from*365))
            #~ qs = qs.filter(q1|q2)
            min_date = today - datetime.timedelta(days=search.aged_from*365)
            qs = qs.filter(birth_date__lte=min_date.strftime("%Y-%m-%d"))
            #~ qs = qs.filter(birth_date__lte=today-datetime.timedelta(days=search.aged_from*365))
        if search.aged_to:
            #~ q1 = models.Q(birth_date__isnull=True)
            #~ q2 = models.Q(birth_date__lte=today-datetime.timedelta(days=search.aged_to*365))
            #~ qs = qs.filter(q1|q2)
            max_date = today - datetime.timedelta(days=search.aged_to*365)
            qs = qs.filter(birth_date__gte=max_date.strftime("%Y-%m-%d"))
            #~ qs = qs.filter(birth_date__gte=today-datetime.timedelta(days=search.aged_to*365))
            
        if search.only_my_persons:
            qs = only_my_persons(qs,search.user)
        
        if search.coached_by:
            qs = only_my_persons(qs,search.coached_by)
            
        if search.period_from:
            qs = only_coached_persons(qs,search.period_from)
            
        if search.period_until:
            qs = only_coached_persons(qs,search.period_until)
          
        required_id_sets = []
        
        required_lk = [lk for lk in search.wantedlanguageknowledge_set.all()]
        if required_lk:
            # language requirements are OR'ed
            ids = set()
            for rlk in required_lk:
                fkw = dict(language__exact=rlk.language)
                if rlk.spoken is not None:
                    fkw.update(spoken__gte=rlk.spoken)
                if rlk.written is not None:
                    fkw.update(written__gte=rlk.written)
                q = LanguageKnowledge.objects.filter(**fkw)
                ids.update(q.values_list('person__id',flat=True))
            required_id_sets.append(ids)
            
        rprops = [x for x in search.wantedskill_set.all()]
        if rprops: # required properties
            ids = set()
            for rp in rprops:
                fkw = dict(property__exact=rp.property) # filter keywords
                if rp.value:
                    fkw.update(value__gte=rp.value)
                q = PersonProperty.objects.filter(**fkw)
                ids.update(q.values_list('person__id',flat=True))
            required_id_sets.append(ids)
          
            
        if required_id_sets:
            s = set(required_id_sets[0])
            for i in required_id_sets[1:]:
                s.intersection_update(i)
                # keep only elements found in both s and i.
            qs = qs.filter(id__in=s)
              
        return qs




class OverlappingContracts(dd.Table):
    model = Person
    use_as_default_report = False
    #~ base_queryset = only_coached_persons(Person.objects.all())
    label = _("Overlapping Contracts")
    #~ def a(self):
        
    
    #~ def get_title(self,rr):
        #~ return _("Primary clients of %s") % rr.master_instance
        
    @classmethod
    def get_request_queryset(self,rr):
        #~ rr.master_instance = rr.get_user()
        qs = super(OverlappingContracts,self).get_request_queryset(rr)
        #~ only_my_persons(qs,rr.get_user())
        qs = only_coached_persons(qs,datetime.date.today())
        #~ qs = qs.filter()
        #~ print 20111118, 'get_request_queryset', rr.user, qs.count()
        return qs



"""
Here we add some specific fields to the 
standard model SiteConfig.
http://osdir.com/ml/django-users/2009-11/msg00696.html
"""

#~ if True: # dd.is_installed('dsbe'):

from lino.models import SiteConfig
dd.inject_field(SiteConfig,
    'job_office',
    #~ models.ForeignKey("contacts.Company",
    models.ForeignKey(settings.LINO.company_model,
        blank=True,null=True,
        verbose_name=_("Local job office"),
        related_name='job_office_sites'),
    """The Company whose contact persons will be 
    choices for `Person.job_office_contact`.
    """)
    
dd.inject_field(SiteConfig,
    'propgroup_skills',
    models.ForeignKey('properties.PropGroup',
        blank=True,null=True,
        verbose_name=_("Skills Property Group"),
        related_name='skills_sites'),
    """The property group to be used as master 
    for the SkillsByPerson report.""")
dd.inject_field(SiteConfig,
    'propgroup_softskills',
    models.ForeignKey('properties.PropGroup',
        blank=True,null=True,
        verbose_name=_("Soft Skills Property Group"),
        related_name='softskills_sites',
        ),
    """The property group to be used as master 
    for the SoftSkillsByPerson report."""
    )
dd.inject_field(SiteConfig,
    'propgroup_obstacles',
    models.ForeignKey('properties.PropGroup',
        blank=True,null=True,
        verbose_name=_("Obstacles Property Group"),
        related_name='obstacles_sites',
        ),
    """The property group to be used as master 
    for the ObstaclesByPerson report."""
    )

dd.inject_field(SiteConfig,
    'residence_permit_upload_type',
    #~ UploadType.objects.get(pk=2)
    models.ForeignKey("uploads.UploadType",
        blank=True,null=True,
        verbose_name=_("Upload Type for residence permit"),
        related_name='residence_permit_sites'),
    """The UploadType for `Person.residence_permit`.
    """)
    
dd.inject_field(SiteConfig,
    'work_permit_upload_type',
    #~ UploadType.objects.get(pk=2)
    models.ForeignKey("uploads.UploadType",
        blank=True,null=True,
        verbose_name=_("Upload Type for work permit"),
        related_name='work_permit_sites'),
    """The UploadType for `Person.work_permit`.
    """)

dd.inject_field(SiteConfig,
    'driving_licence_upload_type',
    #~ UploadType.objects.get(pk=2)
    models.ForeignKey("uploads.UploadType",
        blank=True,null=True,
        verbose_name=_("Upload Type for driving licence"),
        related_name='driving_licence_sites'),
    """The UploadType for `Person.driving_licence`.
    """)
    
dd.inject_field(Company,
    'is_courseprovider',
    mti.EnableChild('dsbe.CourseProvider',verbose_name=_("is Course Provider")),
    """Whether this Company is also a Course Provider."""
    )



"""
...
"""
if settings.LINO.user_model:
    User.grid_search_field = 'username'
    dd.inject_field(User,
        'is_spis',
        models.BooleanField(
            verbose_name=_("is SPIS user")
        ),"""Whether this user is an integration assistant (not a general social agent).
        Deserves more documentation.
        """)
        
RoleType = resolve_model('contacts.RoleType')
#~ RoleType = resolve_model('links.LinkType')
if not isinstance(RoleType,UnresolvedModel):
    """
    autodoc imports this module with :mod:`lino.apps.std.settings` 
    which has no contacts app.
    """
    dd.inject_field(RoleType,
        'use_in_contracts',
        models.BooleanField(
            verbose_name=_("usable in contracts"),
            default=True
        ),"""Whether Links of this type can be used as contact person of a job contract.
        Deserves more documentation.
        """)
        




"""
Here is how we install case-insensitive sorting in sqlite3.
Note that this caused noticeable performance degradation...

Thanks to 
- http://efreedom.com/Question/1-3763838/Sort-Order-SQLite3-Umlauts
- http://docs.python.org/library/sqlite3.html#sqlite3.Connection.create_collation
- http://www.sqlite.org/lang_createindex.html
"""
from django.db.backends.signals import connection_created

def belgian(s):
  
    s = s.decode('utf-8').lower()
    
    s = s.replace(u'ä',u'a')
    s = s.replace(u'à',u'a')
    s = s.replace(u'â',u'a')
    
    s = s.replace(u'ç',u'c')
    
    s = s.replace(u'é',u'e')
    s = s.replace(u'è',u'e')
    s = s.replace(u'ê',u'e')
    s = s.replace(u'ë',u'e')
    
    s = s.replace(u'ö',u'o')
    s = s.replace(u'õ',u'o')
    s = s.replace(u'ô',u'o')
    
    s = s.replace(u'ß',u'ss')
    
    s = s.replace(u'ù',u'u')
    s = s.replace(u'ü',u'u')
    s = s.replace(u'û',u'u')
    
    return s
    
def stricmp(str1, str2):
    return cmp(belgian(str1),belgian(str2))
    
def my_callback(sender,**kw):
    from django.db.backends.sqlite3.base import DatabaseWrapper
    if sender is DatabaseWrapper:
        db = kw['connection']
        db.connection.create_collation('BINARY', stricmp)

connection_created.connect(my_callback)

#~ class ContactPersons(links.LinksFromThis):
    #~ label = _("Contact persons")
    