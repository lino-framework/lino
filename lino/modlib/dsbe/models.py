#coding: UTF-8
## Copyright 2008-2011 Luc Saffre
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
See :doc:`/dsbe/models`

"""

import os
import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode 

#~ import lino
#~ logger.debug(__file__+' : started')

from lino import reports
#~ from lino import layouts
from lino.utils import perms
#~ from lino.utils import printable
from lino import mixins
from lino import fields
from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
from lino.modlib.links import models as links
from lino.modlib.uploads import models as uploads
#~ from lino.modlib.uploads.models import UploadsByPerson
from lino.models import get_site_config
from lino.tools import get_field
from lino.tools import resolve_field
from lino.utils.babel import add_babel_field, default_language, babelattr, babeldict_getitem
from lino.utils.choosers import chooser
from lino.mixins.printable import DirectPrintAction
from lino.mixins.reminder import ReminderEntry

#~ from lino.modlib.fields import KNOWLEDGE_CHOICES # for makemessages


SCHEDULE_CHOICES = {
    'de':[ 
        u"5-Tage-Woche",
        u"Montag, Mittwoch, Freitag",
        u"Individuell",
        ],
    'fr':[ 
        u"5 jours/semaine",
        u"lundi,mercredi,vendredi",
        u"individuel",
        ],
    'en':[
        u"5 days/week",
        u"Monday, Wednesday, Friday",
        u"Individual",
        ]
}

REGIME_CHOICES = {
    'de':[ 
        u"20 Stunden/Woche",
        u"35 Stunden/Woche",
        u"38 Stunden/Woche",
        ],
    'fr':[ 
        u"20 heures/semaine",
        u"35 heures/semaine",
        u"38 heures/semaine",
        ],
    'en':[
        u"20 hours/week",
        u"35 hours/week",
        u"38 hours/week",
        u"38 hours/week",
        ]
}

#~ AID_RATE_CHOICES = {
    #~ 'de':[ 
        #~ u'Alleinlebende Person',
        #~ u'Zusammenlebende Person',
        #~ u'Person mit Familie zu Lasten',
        #~ ],
    #~ 'fr':[ 
        #~ u'Personne isolée',
        #~ u'Personne cohabitante',
        #~ u'Personne qui cohabite avec une famille à sa charge',
        #~ ],
    #~ 'en':[
        #~ ]
#~ }

#~ AID_NATURE_CHOICES = {
    #~ 'de':[ 
        #~ u'Eingliederungseinkommen',
        #~ u'Sozialhilfe', 
        #~ u'Ausgleich zum Eingliederungseinkommen', 
        #~ u'Ausgleich zur Sozialhilfe' 
        #~ ],
    #~ 'fr':[ 
        #~ u"Revenu d'intégration sociale",
        #~ u"Aide sociale",
        #~ u"Complément au revenu d'intégration sociale",
        #~ u"Complément à l'aide sociale",
        #~ ],
    #~ 'en':[
        #~ ]
#~ }

def language_choices(language,choices):
    l = choices.get(language,None)
    if l is None:
        l = choices.get(default_language())
    return l


CIVIL_STATE_CHOICES = [
  ('1', _("single")   ),
  ('2', _("married")  ),
  ('3', _("divorced") ),
  ('4', _("widowed")  ),
  ('5', _("separated")  ), # Getrennt von Tisch und Bett / 
]

# http://en.wikipedia.org/wiki/European_driving_licence

#~ DRIVING_LICENSE_CHOICES = (
  #~ ('A'  , _("Motorcycles") ),
  #~ ('B'  , _("Car") ), # Auto
  #~ ('C'  , _("Lorry") ),
  #~ ('CE' , _("Lorry with trailer") ), 
  #~ ('D'  , _("Bus") ), 
#~ )

RESIDENCE_TYPE_CHOICES = (
  (1  , _("Registry of citizens")   ), # Bevölkerungsregister registre de la population
  (2  , _("Registry of foreigners") ), # Fremdenregister        Registre des étrangers      vreemdelingenregister 
  (3  , _("Waiting for registry")   ), # Warteregister
)

BEID_CARD_TYPES = {
  '1' : dict(en=u"Belgian citizen"),
  '6' : dict(en=u"Kids card (< 12 year)"),
  '8' : dict(en=u"Habilitation",fr=u"Habilitation",nl=u"Machtiging"),
  '11' : dict(
        en=u"Foreigner card type A",
        nl=u"Bewijs van inschrijving in het vreemdelingenregister - Tijdelijk verblijf",
        fr=u"Certificat d'inscription au registre des étrangers - Séjour temporaire",
        de=u"Bescheinigung der Eintragung im Ausländerregister - Vorübergehender Aufenthalt",
      ),
  '12' : dict(
        en=u"Foreigner card type B",
        nl=u"Bewijs van inschrijving in het vreemdelingenregister",
        fr=u"Certificat d'inscription au registre des étrangers",
        de=u"Bescheinigung der Eintragung im Ausländerregister",
      ),
  '13' : dict(
        en=u"Foreigner card type C",
        nl=u"Identiteitskaart voor vreemdeling",
        fr=u"Carte d'identité d'étranger",
        de=u"Personalausweis für Ausländer",
      ),
  '14' : dict(
        en=u"Foreigner card type D",
        nl=u"EG - langdurig ingezetene",
        fr=u"Résident de longue durée - CE",
        de=u"Daueraufenthalt - EG",
      ),
  '15' : dict(
        en=u"Foreigner card type E",
        nl=u"Verklaring van inschrijving",
        fr=u"Attestation d’enregistrement",
        de=u"Anmeldebescheinigung",
      ),
  '16' : dict(
        en=u"Foreigner card type E+",
      ),
  '17' : dict(
        en=u"Foreigner card type F",
        nl=u"Verblijfskaart van een familielid van een burger van de Unie",
        fr=u"Carte de séjour de membre de la famille d’un citoyen de l’Union",
        de=u"Aufenthaltskarte für Familienangehörige eines Unionsbürgers",
      ),
  '18' : dict(
        en=u"Foreigner card type F+",
      ),
}



class Partner(mixins.DiffingMixin,models.Model):
    """
    """
    class Meta:
        app_label = 'contacts'
        abstract = True
  
    id = models.AutoField(primary_key=True,verbose_name=_("Partner #"))
    #~ id = models.CharField(max_length=10,primary_key=True,verbose_name=_("ID"))
    
    is_active = models.BooleanField(verbose_name=_("is active"),default=True)
    "Indicates whether this Contact may be used when creating new operations."
    
    activity = models.ForeignKey("dsbe.Activity",blank=True,null=True,
        verbose_name=_("Activity"))
    "Pointer to :class:`dsbe.Activity`. May be empty."
    
    bank_account1 = models.CharField(max_length=40,blank=True,null=True,
        verbose_name=_("Bank account 1"))
        
    bank_account2 = models.CharField(max_length=40,blank=True,null=True,
        verbose_name=_("Bank account 2"))
        
    def save(self,*args,**kw):
        self.before_save()
        r = super(Partner,self).save(*args,**kw)
        return r
        
    def before_save(self):
        if self.id is None:
            sc = get_site_config()
            if sc.next_partner_id is not None:
                self.id = sc.next_partner_id
                sc.next_partner_id += 1
                sc.save()
        
    def disable_delete(self,request):
        if settings.TIM2LINO_IS_IMPORTED_PARTNER(self):
            return _("Cannot delete companies and persons imported from TIM")
          



class Person(Partner,contacts.Person):
    """
    Implements :class:`contacts.Person`.
    
    This is also Printable just to demonstrate that not only Notes are printables.
    
    Inner class Meta is necessary because of :doc:`/tickets/14`.
    """
    
    class Meta(contacts.Person.Meta):
        app_label = 'contacts'
        verbose_name = _("person")
        verbose_name_plural = _("persons")
        
    #~ first_name = models.CharField(max_length=200,blank=True,verbose_name=_('First name'))
    #~ last_name = models.CharField(max_length=200,blank=True,verbose_name=_('Last name'))
    #~ title = models.CharField(max_length=200,blank=True,verbose_name=_('Title'))
        
    def disabled_fields(self,request):
        if settings.TIM2LINO_IS_IMPORTED_PARTNER(self):
            return PERSON_TIM_FIELDS
        return []
        
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
        
    gesdos_id = models.CharField(max_length=40,blank=True,null=True,
        verbose_name=_("Gesdos ID"))
        
    is_cpas = models.BooleanField(verbose_name=_("receives social help"))
    is_senior = models.BooleanField(verbose_name=_("is senior"))
    #~ is_minor = models.BooleanField(verbose_name=_("is minor"))
    group = models.ForeignKey("dsbe.PersonGroup",blank=True,null=True,
        verbose_name=_("Group"))
    #~ is_dsbe = models.BooleanField(verbose_name=_("is coached"),default=False)
    "Indicates whether this Person is coached."
    
    coached_from = models.DateField(
        blank=True,null=True,
        verbose_name=_("Coached from"))
    coached_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("until"))
    
    coach1 = models.ForeignKey("auth.User",blank=True,null=True,
        verbose_name=_("Coach 1"),related_name='coached1')
    coach2 = models.ForeignKey("auth.User",blank=True,null=True,
        verbose_name=_("Coach 2"),related_name='coached2')
        
    sex = models.CharField(max_length=1,blank=True,null=True,
        verbose_name=_("Sex"),
        choices=(('M',_('Male')),('F',_('Female')))) 
    birth_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("Birth date"))
    birth_date_circa = models.BooleanField(
        default=False,
        verbose_name=_("not exact"))
    birth_place = models.CharField(_("Birth place"),
        max_length=200,
        blank=True,null=True)
    birth_country = models.ForeignKey("countries.Country",
        blank=True,null=True,
        verbose_name=_("Birth country"),related_name='by_birth_place')
    civil_state = models.CharField(max_length=1,
        blank=True,null=True,
        verbose_name=_("Civil state"),
        choices=CIVIL_STATE_CHOICES) 
    national_id = models.CharField(max_length=200,blank=True,verbose_name=_("National ID"))
    
    health_insurance = models.ForeignKey("contacts.Company",blank=True,null=True,
        verbose_name=_("Health insurance"),related_name='health_insurance_for')
    pharmacy = models.ForeignKey("contacts.Company",blank=True,null=True,
        verbose_name=_("Pharmacy"),related_name='pharmacy_for')
    
    nationality = models.ForeignKey('countries.Country',
        blank=True,null=True,
        related_name='by_nationality',
        verbose_name=_("Nationality"))
    #~ tim_nr = models.CharField(max_length=10,blank=True,null=True,unique=True,
        #~ verbose_name=_("TIM ID"))
    card_number = models.CharField(max_length=20,blank=True,null=True,
        verbose_name=_("eID card number"))
    card_valid_from = models.DateField(
        blank=True,null=True,
        verbose_name=_("ID card valid from"))
    card_valid_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("until"))
        
    card_type = models.CharField(max_length=20,blank=True,null=True,
        verbose_name=_("eID card type"))
    card_issuer = models.CharField(max_length=50,blank=True,null=True,
        verbose_name=_("eID card issuer"))
    noble_condition = models.CharField(max_length=50,blank=True,null=True,
        verbose_name=_("noble condition"))
    #~ driving_license = models.ForeignKey("dsbe.DrivingLicense",blank=True,null=True,
        #~ verbose_name=_("Driving license"))
    #~ driving_license = models.CharField(max_length=4,blank=True,null=True,
        #~ verbose_name=_("Driving license"),choices=DRIVING_LICENSE_CHOICES)
    
    no_shift = models.BooleanField(verbose_name=_("no shift work"))
    no_weekend = models.BooleanField(verbose_name=_("no work on week-end"))
    has_family = models.BooleanField(verbose_name=_("Head of a family"))
    
    
    has_own_car = models.BooleanField(verbose_name=_("has own car"))
    
    can_car = models.BooleanField(verbose_name=_("Car driving license"))
    can_truck = models.BooleanField(verbose_name=_("Truck driving license"))
    can_clark = models.BooleanField(verbose_name=_("Clark driving license"))
    can_bus = models.BooleanField(verbose_name=_("Bus driving license"))
    
    #~ driving_license_until = models.DateField(_("Driving license valid until"),blank=True,null=True)
    
    it_knowledge = fields.KnowledgeField(blank=True,null=True,
        verbose_name=_("IT knowledge"))
        
    #~ residence_permit_until = models.DateField(blank=True,null=True,verbose_name=_("Residence permit valid until"))
    residence_type = models.SmallIntegerField(blank=True,null=True,
        verbose_name=_("Residence type"),
        choices=RESIDENCE_TYPE_CHOICES,
        max_length=1,
        #~ limit_to_choices=True,
        )
    in_belgium_since = models.DateField(_("Lives in Belgium since"),blank=True,null=True)
    unemployed_since = models.DateField(_("Seeking work since"),blank=True,null=True)
    #~ work_permit_exempt = models.BooleanField(verbose_name=_("Work permit exemption"))
    needs_residence_permit = models.BooleanField(verbose_name=_("Needs residence permit"))
    needs_work_permit = models.BooleanField(verbose_name=_("Needs work permit"))
    #~ work_permit_valid_until = models.DateField(blank=True,null=True,verbose_name=_("Work permit valid until"))
    work_permit_suspended_until = models.DateField(blank=True,null=True,verbose_name=_("suspended until"))
    aid_type = models.ForeignKey("dsbe.AidType",blank=True,null=True,
        verbose_name=_("aid type"))
        
    income_ag    = models.BooleanField(verbose_name=_("Arbeitslosengeld"))
    income_wg    = models.BooleanField(verbose_name=_("Wartegeld"))
    income_kg    = models.BooleanField(verbose_name=_("Krankengeld"))
    income_rente = models.BooleanField(verbose_name=_("Rente"))
    income_misc  = models.BooleanField(verbose_name=_("Andere"))
    
    
    physical_handicap = models.BooleanField(_("Physical handicap"))
    mental_handicap = models.BooleanField(_("Mental handicap"))
    psycho_handicap = models.BooleanField(_("Psychological handicap"))
    health_problems = models.BooleanField(_("Health problems"))
    juristic_problems = models.BooleanField(_("Juristic problems"))
    dependency_problems = models.BooleanField(_("Dependency problems"))
    social_competence = models.BooleanField(_("Lack of social competence"))
    motivation_lack = models.BooleanField(_("Lack of motivation"))
    
    unavailable_until = models.DateField(blank=True,null=True,verbose_name=_("Unavailable until"))
    unavailable_why = models.CharField(max_length=100,blank=True,null=True,
        verbose_name=_("reason"))
    
    fulltime_only = models.BooleanField(_("Fulltime only"))
    parttime_only = models.BooleanField(_("Part-time only"))
    young_children = models.BooleanField(_("Young children"))
    native_language = models.ForeignKey('countries.Language',
      verbose_name=_("Native language"),
      blank=True,null=True)
    is_illiterate = models.BooleanField(_("Illiterate"))
    #~ native_language = fields.LanguageField(
      #~ verbose_name=_("Native language"),
      #~ blank=True,null=True)
    #~ native_language = models.CharField(max_length=100,
        #~ blank=True,null=True,
        #~ verbose_name=_("Native language"))
    #~ migration = models.BooleanField(_("Migration"))
    is_seeking = models.BooleanField(_("is seeking work"))
    
    obstacles = models.TextField(_("Obstacles"),blank=True,null=True)
    skills = models.TextField(_("Other skills"),blank=True,null=True)
    job_agents = models.CharField(max_length=100,
        blank=True,null=True,
        verbose_name=_("Job agents"))
    
    job_office_contact = models.ForeignKey("contacts.Contact",
      blank=True,null=True,
      verbose_name=_("Contact person at local job office"),
      related_name='persons_job_office')
      
    @chooser()
    def job_office_contact_choices(cls):
        sc = get_site_config()
        if sc.job_office is not None:
        #~ pk = settings.LINO_SITE.job_office_id
        #~ if pk is not None:
            #~ jo = Company.objects.get(pk=pk)
            #~ return jo.contact_set.all()
            return sc.job_office.contact_set.all()
        return []


    @classmethod
    def setup_report(model,rpt):
        rpt.add_action(DirectPrintAction(rpt,'auskblatt',_("Auskunftsblatt"),'appypdf','persons/auskunftsblatt.odt'))
        rpt.add_action(DirectPrintAction(rpt,'eid',_("eID-Inhalt"),'appypdf','persons/eid-content.odt'))
        rpt.add_action(DirectPrintAction(rpt,'cv',_("Curiculum vitae"),'appypdf','persons/cv.odt'))
        
    def __unicode__(self):
        return u"%s (%s)" % (self.name,self.pk)
        
    def clean(self):
        if self.job_office_contact:
            #~ print "Person.clean()", self
            if self.job_office_contact.person == self:
                raise ValidationError(_("Circular reference"))
        super(Person,self).clean()
        
    full_name = property(contacts.Person.get_full_name)
    
    def card_type_text(self,request):
        if self.card_type:
            s = babeldict_getitem(BEID_CARD_TYPES,self.card_type)
            if s:
                return s
        return self.card_type
    card_type_text.return_type = fields.DisplayField(_("eID card type"))
        
    def get_print_language(self,pm):
        "Used by DirectPrintAction"
        return self.language
        
    @classmethod
    def get_reminders(model,today,user):
        q = models.Q(coach1__exact=user) | models.Q(coach2__exact=user)
        
        def find_them(fieldname,today,d,msg,**linkkw):
            filterkw = { fieldname+'__lte' : today + d }
            for obj in model.objects.filter(q,**filterkw).order_by(fieldname):
                yield ReminderEntry(obj,getattr(obj,fieldname),msg,**linkkw)
            
        #~ delay = 30
        #~ for obj in model.objects.filter(q,
              #~ card_valid_until__lte=date+datetime.timedelta(days=delay)).order_by('card_valid_until'):
            #~ yield ReminderEntry(obj,obj.card_valid_until,_("eID card expires in %d days") % delay,fmt='detail',tab=3)
        for o in find_them('card_valid_until', today, datetime.timedelta(days=30),
            _("eID card expires"),fmt='detail',tab=0):
            yield o
        for o in find_them('unavailable_until', today, datetime.timedelta(days=30),
            _("becomes available again"),fmt='detail',tab=1):
            yield o
        for o in find_them('work_permit_suspended_until', today, datetime.timedelta(days=30),
              _("work permit suspension ends"),fmt='detail',tab=1):
            yield o
        for o in find_them('coached_until', today, datetime.timedelta(days=30),
            _("coaching ends"),fmt='detail',tab=1):
            yield o
            
            #~ todo... delay=(value, unit)
        #~ for obj in model.objects.filter(q,
              #~ driving_license_until__lte=date+datetime.timedelta(days=14)).order_by('driving_license_until'):
            #~ yield ReminderEntry(obj,obj.driving_license_until,_("driving license expires in 14 days"),fmt='detail',tab=3)
        #~ for obj in model.objects.filter(q,
              #~ residence_permit_until__lte=date+datetime.timedelta(days=60)).order_by('residence_permit_until'):
            #~ yield ReminderEntry(obj,obj.residence_permit_until,_("residence permit expires in 60 days"),fmt='detail',tab=4)
        #~ for obj in model.objects.filter(q,
              #~ work_permit_valid_until__lte=date+datetime.timedelta(days=40)).order_by('work_permit_valid_until'):
            #~ yield ReminderEntry(obj,obj.work_permit_valid_until,_("work permit expires in 40 days"),fmt='detail',tab=4)
      
        
    def get_image_parts(self):
        if self.card_number:
            return ("beid",self.card_number+".jpg")
        return ("pictures","contacts.Person.jpg")
    def get_image_url(self):
        return settings.MEDIA_URL + "/".join(self.get_image_parts())
    def get_image_path(self):
        return os.path.join(settings.MEDIA_ROOT,*self.get_image_parts())
        
            
    #~ def is_illiterate(self):
        #~ if self.languageknowledge_set.count() == 0:
            #~ return False
        #~ for lk in self.languageknowledge_set.all():
            #~ if lk.written > 0:
                #~ return False
        #~ return True
    #~ is_illiterate.return_type = models.BooleanField(_("Illiterate"),editable=False)
    
    def age(self,request):
        if self.birth_date:
            dd = datetime.date.today()-self.birth_date
            return _("%d years") % (dd.days / 365)
        return _('unknown')
    age.return_type = fields.DisplayField(_("Age"))
    #~ age.return_type = models.CharField(_("Age"),max_length=10,editable=False,blank=True)
    
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
    overview.return_type = fields.HtmlBox(_("Overview"))
    
    def work_permit(self,rr):
        #~ return uploads.UploadsByPerson().request(master_instance=self,type__exact=3)
        rrr = rr.spawn_request(uploads.UploadsByPerson(),master_instance=self,
            known_values=dict(type=settings.LINO_SITE.upload_work_permit_type))
        return rr.ui.quick_upload_buttons(rrr)
    work_permit.return_type = fields.DisplayField(_("Work permit"))
    
    def residence_permit(self,rr):
        #~ return uploads.UploadsByPerson().request(master_instance=self,type__exact=2)
        rrr = rr.spawn_request(uploads.UploadsByPerson(),master_instance=self,
            known_values=dict(type=settings.LINO_SITE.upload_residence_permit_type))
        return rr.ui.quick_upload_buttons(rrr)
    residence_permit.return_type = fields.DisplayField(_("Residence permit"))
    
    def driving_license(self,rr):
        rrr = rr.spawn_request(uploads.UploadsByPerson(),
            master_instance=self,
            known_values=dict(type=settings.LINO_SITE.upload_diving_licence_type))
        return rr.ui.quick_upload_buttons(rrr)
        #~ return uploads.UploadsByPerson().request(master_instance=self,type__exact=5)
    #~ driving_license.return_type = fields.ShowOrCreateButton(_("driving license"))
    driving_license.return_type = fields.DisplayField(_("driving license"))
    
    
PERSON_TIM_FIELDS = reports.fields_list(Person,
    '''name first_name last_name title remarks
    zip_code city country street street_no street_box 
    birth_date sex birth_place coach1 language 
    phone fax email 
    card_number card_valid_from card_valid_until
    national_id health_insurance pharmacy 
    bank_account1 bank_account2 
    gesdos_id activity 
    is_cpas is_senior is_active nationality''')



class Persons(contacts.Persons):
    can_view = perms.is_authenticated
    app_label = 'contacts'
    #~ extra = dict(
      #~ select=dict(sort_name='lower(last_name||first_name)'),
      #~ order_by=['sort_name'])
    #~ order_by = None # clear the default value from contacts.Persons.order_by since we use extra order_by

    
class PersonsByNationality(Persons):
    #~ app_label = 'contacts'
    fk_name = 'nationality'
    order_by = "city name".split()
    column_names = "city street street_no street_box addr2 name country language *"
    
class PersonsByCity(Persons):
    #~ app_label = 'contacts'
    fk_name = 'city'
    order_by = 'street street_no street_box addr2'.split()
    column_names = "street street_no street_box addr2 name language *"

class MyPersons(Persons):
    use_as_default_report = False
    label = _("My coached Persons")
    order_by = ['last_name','first_name']
    #~ def get_queryset(self):
    def get_request_queryset(self,rr):
        today = datetime.date.today()
        qs = super(MyPersons,self).get_request_queryset(rr)
        Q = models.Q
        q1 = Q(coach1__exact=rr.user) | Q(coach2__exact=rr.user)
        #~ q3 = Q(group__isnull=False)
        #~ q3 = Q(coached_from__isnull=False) | Q(coached_until__isnull=False)
        q2 = Q(coached_from__isnull=False) | Q(coached_until__isnull=False,coached_until__gte=today)
        #~ q2 = Q(coached__gt=0)
        #~ q2 = Q(dsbe_coach__exact=user)
        #~ q2 = Q(dsbe_coaches__contains=user)
        #~ q2 = Q(coaching_set__user__exact=user)
        #~ return Person.objects.annotate(dsbe_ccoach=Count('coaching_set__user__exact')).filter(q1|q2)
        return qs.filter(q1,q2)
    #~ Person.user == user 
    #~ or 
    #~ Person.coachings_set.filter(user__exact=user).count() > 0        

class MyPersonsByGroup(MyPersons):
    fk_name = 'group'
              
#~ class Company(Contact,contacts.Company):
#~ class Company(Partner,contacts.Addressable,):
class Company(Partner,contacts.Company):
  
    """
    Implements :class:`contacts.Company`.
    
    Inner class Meta is necessary because of :doc:`/tickets/14`.
    """
    
    class Meta(contacts.Company.Meta):
        app_label = 'contacts'
        verbose_name = _("company")
        verbose_name_plural = _("companies")
    #~ vat_id = models.CharField(max_length=200,blank=True)
    #~ type = models.ForeignKey('contacts.CompanyType',blank=True,null=True,verbose_name=_("Company type"))
    prefix = models.CharField(max_length=200,blank=True) 
    hourly_rate = fields.PriceField(_("hourly rate"),blank=True,null=True)
    is_courseprovider = models.BooleanField(_("Course provider")) 
    
    def disabled_fields(self,request):
        if settings.TIM2LINO_IS_IMPORTED_PARTNER(self):
            return COMPANY_TIM_FIELDS
        return []
    
COMPANY_TIM_FIELDS = reports.fields_list(Company,
    '''name remarks
    zip_code city country street street_no street_box 
    language vat_id
    phone fax email 
    bank_account1 bank_account2 activity''')
  
    
class Companies(contacts.Companies):
    app_label = 'contacts'
    #~ pass
    
#~ from lino.modlib.contacts.models import Companies

#
# PERSON GROUP
#
class PersonGroup(models.Model):
    name = models.CharField(_("Designation"),max_length=200)
    #~ text = models.TextField(_("Description"),blank=True,null=True)
    class Meta:
        verbose_name = _("person group")
        verbose_name_plural = _("person groups")
    def __unicode__(self):
        return self.name

class PersonGroups(reports.Report):
    model = PersonGroup
    order_by = ["name"]

    
#
# STUDY TYPE
#
class StudyType(models.Model):
    name = models.CharField(_("Designation"),max_length=200)
    #~ text = models.TextField(_("Description"),blank=True,null=True)
    class Meta:
        verbose_name = _("study type")
        verbose_name_plural = _("study types")
    def __unicode__(self):
        return self.name

class StudyTypes(reports.Report):
    #~ label = _('Study types')
    model = StudyType
    order_by = ["name"]

#
# STUDY CONTENT
#
#~ class StudyContent(models.Model):
    #~ type = models.ForeignKey(StudyType)
    #~ name = models.CharField(max_length=200,verbose_name=_("Designation"))
    #~ text = models.TextField(blank=True,null=True)
    #~ def __unicode__(self):
        #~ return self.name

#~ class StudyContents(reports.Report):
    #~ label = _('Study contents')
    #~ model = StudyContent
    #~ order_by = "name"
    
#~ class StudyContentsByType(StudyContents):
    #~ fk_name = 'type'

#
# Study
#


class Study(models.Model):
    class Meta:
        verbose_name = _("study or education")
        verbose_name_plural = _("Studies & education")
    person = models.ForeignKey("contacts.Person",verbose_name=_("Person"))
    type = models.ForeignKey(StudyType,verbose_name=_("Study type"))
    content = models.CharField(max_length=200,blank=True,null=True,verbose_name=_("Study content"))
    #~ content = models.ForeignKey(StudyContent,blank=True,null=True,verbose_name=_("Study content"))
  
    started = fields.MonthField(_("started"),blank=True,null=True)
    stopped = fields.MonthField(_("stopped"),blank=True,null=True)
    #~ started = models.DateField(blank=True,null=True,verbose_name=_("started"))
    #~ stopped = models.DateField(blank=True,null=True,verbose_name=_("stopped"))
    #~ started = fields.MonthField(blank=True,null=True,verbose_name=_("started"))
    #~ stopped = fields.MonthField(blank=True,null=True,verbose_name=_("stopped"))
    success = models.BooleanField(verbose_name=_("Success"),default=False)
    country = models.ForeignKey("countries.Country",blank=True,null=True,
        verbose_name=_("Country"))
    city = models.ForeignKey('countries.City',blank=True,null=True,
        verbose_name=_('City'))
    language = models.ForeignKey("countries.Language",blank=True,null=True,verbose_name=_("Language"))
    #~ language = fields.LanguageField(blank=True,null=True,verbose_name=_("Language"))
    
    school = models.CharField(max_length=200,blank=True,null=True,verbose_name=_("School"))
    #~ school = models.ForeignKey("contacts.Company",blank=True,null=True,verbose_name=_("School"))
    
    remarks = models.TextField(blank=True,null=True,verbose_name=_("Remarks"))
    
    def __unicode__(self):
        return unicode(self.type)
  
    @chooser()
    def city_choices(cls,country):
        if country is not None:
            return country.city_set.order_by('name')
        return cls.city.field.rel.to.objects.order_by('name')
        
class StudiesByPerson(reports.Report):
    model = Study
    fk_name = 'person'
    #~ label = _("Studies & experiences")
    button_label = _("Studies")
    order_by = ["started"]
    
    
#
# LanguageKnowledge
#

class LanguageKnowledge(models.Model):
    class Meta:
        verbose_name = _("language knowledge")
        verbose_name_plural = _("language knowledges")
        
    person = models.ForeignKey("contacts.Person")
    language = models.ForeignKey("countries.Language",verbose_name=_("Language"))
    #~ language = models.ForeignKey("countries.Language")
    #~ language = fields.LanguageField()
    spoken = fields.KnowledgeField(verbose_name=_("spoken"))
    written = fields.KnowledgeField(verbose_name=_("written"))
    
    def __unicode__(self):
        if self.spoken > '1' and self.written > '1':
            return _(u"%s (s/w)") % self.language
        elif self.spoken > '1':
            return _(u"%s (s)") % self.language
        elif self.written > '1':
            return _(u"%s (w)") % self.language
        else:
            return unicode(self.language)
      
    
class LanguageKnowledgesByPerson(reports.Report):
    model = LanguageKnowledge
    fk_name = 'person'
    #~ label = _("Language knowledge")
    #~ button_label = _("Languages")
    column_names = "language spoken written"
  
#
# Skills
#

class SkillType(models.Model):
    class Meta:
        verbose_name = _("Skill type")
        verbose_name_plural = _("Skill types")
    name = models.CharField(max_length=200,verbose_name=_("Designation"))
    
    def __unicode__(self):
        return babelattr(self,'name')

add_babel_field(SkillType,'name')

class SkillTypes(reports.Report):
    model = SkillType
    order_by = ['name']



class Skill(models.Model):
    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        
    person = models.ForeignKey("contacts.Person")
    type = models.ForeignKey(SkillType,blank=True,null=True,
      verbose_name=_("skill type"))
    #~ type = models.ForeignKey("dsbe.JobType")
    strength = fields.StrengthField(verbose_name=_("strength"))
    remark = models.CharField(max_length=200,
        blank=True,null=True,
        verbose_name=_("Remark"))
    
class SkillsByPerson(reports.Report):
    model = Skill
    fk_name = 'person'
    column_names = "type strength"
    
#
# JOBS
#

#~ class JobType(models.Model):
    #~ name = models.CharField(_("Designation"),max_length=200)
    #~ class Meta:
        #~ verbose_name = _("job type")
        #~ verbose_name_plural = _("job types")
    #~ def __unicode__(self):
        #~ return self.name

#~ class JobTypes(reports.Report):
    #~ model = JobType
    #~ order_by = ["name"]

#~ class JobWish(models.Model):
    #~ class Meta:
        #~ verbose_name = _("job wish")
        #~ verbose_name_plural = _("job wishes")
        
    #~ person = models.ForeignKey("contacts.Person")
    #~ type = models.ForeignKey('contacts.ContactType',blank=True,null=True,
      #~ verbose_name=_("contact type"))
    #~ strength = fields.StrengthField(verbose_name=_("strength"))
    
#~ class JobWishesByPerson(reports.Report):
    #~ model = JobWish
    #~ fk_name = 'person'
    #~ column_names = "type strength"
    
    
class JobExperience(models.Model):
    class Meta:
        verbose_name = _("job experience")
        verbose_name_plural = _("job experiences")
    person = models.ForeignKey("contacts.Person",verbose_name=_("Person"))
    #~ company = models.ForeignKey("contacts.Company",verbose_name=_("Company"))
    company = models.CharField(max_length=200,verbose_name=_("company"))
    #~ type = models.ForeignKey(JobType,verbose_name=_("job type"))
    title = models.CharField(max_length=200,verbose_name=_("job title"))
    country = models.ForeignKey("countries.Country",
        blank=True,null=True,
        verbose_name=_("Country"))
  
    started = fields.MonthField(_("started"),blank=True,null=True)
    stopped = fields.MonthField(_("stopped"),blank=True,null=True)
    
    remarks = models.TextField(blank=True,null=True,verbose_name=_("Remarks"))
    
    def __unicode__(self):
        return unicode(self.title)
  
class JobExperiencesByPerson(reports.Report):
    model = JobExperience
    fk_name = 'person'
    order_by = ["started"]
    
  

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

class Activities(reports.Report):
    model = Activity
    #~ label = _('Activities')

#~ class ActivitiesByPerson(Activities):
    #~ fk_name = 'activity'

#~ class ActivitiesByCompany(Activities):
    #~ fk_name = 'activity'
    
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

class ExclusionTypes(reports.Report):
    model = ExclusionType
    #~ label = _('Exclusion Types')
    
#
# EXCLUSIONS (Arbeitslosengeld-Sperrungen)
#
class Exclusion(models.Model):
    class Meta:
        verbose_name = _("exclusion")
        verbose_name_plural = _('exclusions')
        
    person = models.ForeignKey("contacts.Person")
    type = models.ForeignKey("dsbe.ExclusionType",verbose_name=_("Reason"))
    excluded_from = models.DateField(blank=True,null=True,verbose_name=_("from"))
    excluded_until = models.DateField(blank=True,null=True,verbose_name=_("until"))
    remark = models.CharField(max_length=200,blank=True,verbose_name=_("Remark"))
    
    def __unicode__(self):
        s = unicode(self.type)
        if self.excluded_from: s += ' ' +unicode(self.excluded_from)
        if self.excluded_until: s += '-'+unicode(self.excluded_until)
        return s

class Exclusions(reports.Report):
    model = Exclusion
    #~ label = _('Exclusions')
    
class ExclusionsByPerson(Exclusions):
    fk_name = 'person'
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

#~ class CoachingTypes(reports.Report):
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
    

#~ class Coachings(reports.Report):
    #~ model = Coaching
    
#~ class CoachingsByPerson(Coachings):
    #~ fk_name = 'person'
    #~ column_names = 'coach type remark *'
    #~ label = _('Coaches')

#
# CONTRACT TYPES 
#
class ContractType(mixins.PrintableType):
    templates_group = 'contracts'
    class Meta:
        verbose_name = _("contract type")
        verbose_name_plural = _('contract types')
        
    ref = models.CharField(_("reference"),max_length=20,blank=True)
    name = models.CharField(_("contract title"),max_length=200)
    
    def __unicode__(self):
        return unicode(babelattr(self,'name'))
        
add_babel_field(ContractType,'name')

class ContractTypes(reports.Report):
    model = ContractType
    column_names = 'name build_method template *'

#
# EXAMINATION POLICIES
#
class ExamPolicy(models.Model):
    class Meta:
        verbose_name = _("examination policy")
        verbose_name_plural = _('examination policies')
        
    name = models.CharField(_("designation"),max_length=200)
    
    def __unicode__(self):
        return unicode(babelattr(self,'name'))
    #~ def __unicode__(self):
        #~ return unicode(self.name)
        
add_babel_field(ExamPolicy,'name')

class ExamPolicies(reports.Report):
    model = ExamPolicy
    column_names = 'name *'

#
# CONTRACT ENDINGS
#
class ContractEnding(models.Model):
    class Meta:
        verbose_name = _("Contract Ending")
        verbose_name_plural = _('Contract Endings')
        
    name = models.CharField(_("designation"),max_length=200)
    
    def __unicode__(self):
        return unicode(self.name)
        
class ContractEndings(reports.Report):
    model = ContractEnding
    column_names = 'name *'
    order_by = ['name']

#
# COURSE ENDINGS
#
class CourseEnding(models.Model):
    class Meta:
        verbose_name = _("Course Ending")
        verbose_name_plural = _('Course Endings')
        
    name = models.CharField(_("designation"),max_length=200)
    
    def __unicode__(self):
        return unicode(self.name)
        
class CourseEndings(reports.Report):
    model = CourseEnding
    column_names = 'name *'
    order_by = ['name']


#
# AID TYPES
#
class AidType(models.Model):
    class Meta:
        verbose_name = _("aid type")
        verbose_name_plural = _('aid types')
        
    name = models.CharField(_("designation"),max_length=200)
    
    def __unicode__(self):
        return unicode(babelattr(self,'name'))
        
add_babel_field(AidType,'name')

class AidTypes(reports.Report):
    model = AidType
    column_names = 'name *'



#
# CONTRACTS
#
class Contract(mixins.DiffingMixin,mixins.TypedPrintable,mixins.Reminder,mixins.PartnerDocument):
    class Meta:
        verbose_name = _("contract")
        verbose_name_plural = _('contracts')
        
    contact = models.ForeignKey("contacts.Contact",blank=True,null=True,
      verbose_name=_("represented by"))
    #~ user = models.ForeignKey("auth.User",verbose_name=_("Coach"))
    type = models.ForeignKey("dsbe.ContractType",verbose_name=_("contract type"),blank=True)
    language = fields.LanguageField(default=default_language)
    
    applies_from = models.DateField(_("applies from"),blank=True,null=True,)
    applies_until = models.DateField(_("applies until"),blank=True,null=True)
    date_decided = models.DateField(blank=True,null=True,verbose_name=_("date decided"))
    date_issued = models.DateField(blank=True,null=True,verbose_name=_("date issued"))
    duration = models.IntegerField(_("duration (days)"),blank=True,null=True,default=None)
    
    
    regime = models.CharField(_("regime"),max_length=200,blank=True,null=True)
    schedule = models.CharField(_("schedule"),max_length=200,blank=True,null=True)
    hourly_rate = fields.PriceField(_("hourly rate"),blank=True,null=True)
    refund_rate = models.CharField(_("refund rate"),max_length=200,
        blank=True,null=True)
    
    reference_person = models.CharField(_("reference person"),max_length=200,
        blank=True,null=True)
    
    responsibilities = models.TextField(_("responsibilities"),blank=True,null=True)
    
    stages = fields.HtmlTextField(_("stages"),blank=True,null=True)
    goals = fields.HtmlTextField(_("goals"),blank=True,null=True)
    duties_asd = fields.HtmlTextField(_("duties ASD"),blank=True,null=True)
    duties_dsbe = fields.HtmlTextField(_("duties DSBE"),blank=True,null=True)
    duties_company = fields.HtmlTextField(_("duties company"),blank=True,null=True)
    
    user_asd = models.ForeignKey("auth.User",verbose_name=_("responsible (ASD)"),
        related_name='contracts_asd',blank=True,null=True) 
    
    exam_policy = models.ForeignKey("dsbe.ExamPolicy",blank=True,null=True,
        verbose_name=_("examination policy"))
        
    ending = models.ForeignKey("dsbe.ContractEnding",blank=True,null=True,
        verbose_name=_("Ending"))
    date_ended = models.DateField(blank=True,null=True,verbose_name=_("date ended"))
    
    #~ aid_nature = models.CharField(_("aid nature"),max_length=100,blank=True)
    #~ aid_rate = models.CharField(_("aid rate"),max_length=100,blank=True)
    
    @chooser(simple_values=True)
    def duration_choices(cls):
        return [ 312, 468, 624 ]
        #~ return [ 0, 25, 50, 100 ]
    
    @chooser(simple_values=True)
    def regime_choices(cls,language):
        return language_choices(language,REGIME_CHOICES)
    
    @chooser(simple_values=True)
    def schedule_choices(cls,language):
        return language_choices(language,SCHEDULE_CHOICES)
    
    @chooser(simple_values=True)
    def refund_rate_choices(cls):
        return [ 
        u"0%",
        u"25%",
        u"50%",
        u"100%",
        ]
    
    #~ @chooser(simple_values=True)
    #~ def aid_rate_choices(cls,language):
        #~ return language_choices(language,AID_RATE_CHOICES)
        
    #~ @chooser(simple_values=True)
    #~ def aid_nature_choices(cls,language):
        #~ return language_choices(language,AID_NATURE_CHOICES)
    
    #~ @chooser(simple_values=True)
    #~ def exam_policy_choices(cls,language):
        #~ return ExamPolicy.objects.all()
    
    
    def disabled_fields(self,request):
        if self.must_build:
            return []
        return CONTRACT_PRINTABLE_FIELDS
        
    @chooser()
    def contact_choices(cls,company):
        if company is not None:
            return company.contact_set.all()
        return []
        #~ print 'Contract.contact_choices for', company
        #~ choices = company.contact_set.all()
        #~ print 'Contract.contact_choices returns', choices
        #~ return choices
    
    def __unicode__(self):
        msg = _("Contract # %s")
        #~ msg = _("Contract # %(pk)d (%(person)s/%(company)s)")
        #~ return msg % dict(pk=self.pk, person=self.person, company=self.company)
        return msg % self.pk
        
    def summary_row(self,ui,rr,**kw):
        s = ''
        if self.reminder_text:
            s += '<b>' + cgi.escape(self.reminder_text) + '</b> '
        s += ui.href_to(self)
        if self.person:
            if self.company:
                s += "(" + ui.href_to(self.person) + "/" + ui.href_to(self.company) + ")"
            else:
                s += "(" + ui.href_to(self.person) + ")"
        elif self.company:
            s += "(" + ui.href_to(self.company) + ")"
        return s
        
    def dsbe_person(self):
        if self.person_id is not None:
            if self.person.coach2_id is not None:
                return self.person.coach2_id
            return self.person.coach1 or self.user
            
        #~ try:
            #~ return self.person.coaching_set.get(type__name__exact='DSBE').coach        
        #~ except Exception,e:
            #~ return self.person.user or self.user
            
    def on_person_changed(self,request):
        if self.person_id is not None:
            if self.person.coach1_id is None or self.person.coach1_id == self.user_id:
                self.user_asd = None
            else:
                self.user_asd = self.person.coach1
                
    def on_create(self,request):
        super(Contract,self).on_create(request)
        self.on_person_changed(request)
      
    def full_clean(self):
      
        if self.person_id is not None:
            #~ if not self.user_asd:
                #~ if self.person.user != self.user:
                    #~ self.user_asd = self.person.user
            if self.person.birth_date and self.applies_from:
                def duration(refdate):
                    delta = refdate - self.person.birth_date
                    age = delta.days / 365
                    if age < 36:
                        return 312
                    elif age < 50:
                        return 468
                    else:
                        return 624
              
                if self.duration is None:
                    if self.applies_until:
                        self.duration = duration(self.applies_until)
                    else:
                        self.duration = duration(self.applies_from)
                        self.applies_until = self.applies_from + datetime.timedelta(days=self.duration)
                    
        if self.company is not None:
          
            if self.hourly_rate is None:
                self.hourly_rate = self.company.hourly_rate
                
            if self.type_id is None \
                and self.company.type is not None \
                and self.company.type.contract_type is not None:
                self.type = self.company.type.contract_type
        
CONTRACT_PRINTABLE_FIELDS = reports.fields_list(Contract,
  'person company contact type '
  'applies_from applies_until duration '
  'language schedule regime hourly_rate refund_rate reference_person '
  'stages duties_dsbe duties_company duties_asd '
  'user user_asd exam_policy '
  'date_decided date_issued responsibilities')


class Contracts(reports.Report):
    model = Contract
    
class ContractsByPerson(Contracts):
    fk_name = 'person'
    column_names = 'company applies_from applies_until user type *'

        
class ContractsByCompany(Contracts):
    fk_name = 'company'
    column_names = 'person applies_from applies_until user type *'

class ContractsByType(Contracts):
    fk_name = 'type'
    column_names = "applies_from person company user *"
    order_by = ["applies_from"]

class MyContracts(mixins.ByUser,Contracts):
    column_names = "applies_from person company *"
    label = _("My contracts")
    #~ order_by = "reminder_date"
    #~ column_names = "reminder_date person company *"
    order_by = ["applies_from"]
    #~ filter = dict(reminder_date__isnull=False)


#
# NOTES
#
class Note(notes.Note,mixins.PartnerDocument):
    class Meta:
        app_label = 'notes'

class NotesByPerson(notes.Notes):
    fk_name = 'person'
    column_names = "date subject user company *"
    order_by = ["date"]
  
class NotesByCompany(notes.Notes):
    fk_name = 'company'
    column_names = "date subject user person *"
    order_by = ["date"]
  
#
# LINKS
#
class Link(links.Link,mixins.PartnerDocument):
    class Meta:
        app_label = 'links'

class LinksByPerson(links.LinksByOwnerBase):
    fk_name = 'person'
    column_names = "name url user date company *"
    order_by = ["date"]
  
class LinksByCompany(links.LinksByOwnerBase):
    fk_name = 'company'
    column_names = "name url user date person *"
    order_by = ["date"]
    

#
# COURSES
#


#~ class CourseProvider(models.Model):
#~ class CourseProvider(Company):
    #~ """Kursanbieter (KAP, Oikos, Lupe, ...) 
    #~ """
    #~ class Meta:
        #~ app_label = 'dsbe'
    #~ name = models.CharField(max_length=200,
          #~ verbose_name=_("Name"))
    #~ company = models.ForeignKey("contacts.Company",blank=True,null=True,verbose_name=_("Company"))
    
CourseProvider = Company

class CourseProviders(Companies):
    use_as_default_report = False
    #~ app_label = 'dsbe'
    label = _("Course providers")
    model = CourseProvider
    filter = dict(is_courseprovider__exact=True)
    
    def create_instance(self,req,**kw):
        instance = super(CourseProviders,self).create_instance(req,**kw)
        instance.is_courseprovider = True
        return instance
  
class CourseContent(models.Model):
    "Kursinhalte (FR, DE, EN, Alfa)"
    
    class Meta:
        verbose_name = _("Course Content")
        verbose_name_plural = _('Course Contents')
        
    name = models.CharField(max_length=200,
          blank=True,null=True,
          verbose_name=_("Name"))
          
    def __unicode__(self):
        return unicode(self.name)
        
  
class Course(models.Model):
  
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _('Courses')
        
    title = models.CharField(max_length=200,
        verbose_name=_("Name"))
    content = models.ForeignKey("dsbe.CourseContent",
        verbose_name=_("Course content"))
    provider = models.ForeignKey(CourseProvider,
        verbose_name=_("Course provider"))
    @chooser()
    def provider_choices(cls):
        return CourseProviders.request().queryset
    start_date = models.DateField(_("start date"),blank=True,null=True)
    content = models.ForeignKey("dsbe.CourseContent",verbose_name=_("Course content"))
  
    remark = models.CharField(max_length=200,
        blank=True,null=True,
        verbose_name=_("Remark"))
        
    def __unicode__(self):
        if self.start_date is None:
            return u'%s %s' % (self.title,self.provider)
        return u'%s %s %s' % (self.title,self.start_date,self.provider)
  
#~ class CourseRequest(mixins.Reminder):
class CourseRequest(models.Model):
    "Kursanfragen : Person X sucht einen Kurs mit Inhalt Y"
    class Meta:
        verbose_name = _("Course Requests")
        verbose_name_plural = _('Course Requests')
        
    person = models.ForeignKey("contacts.Person",
        verbose_name=_("Person"))
    content = models.ForeignKey("dsbe.CourseContent",
        verbose_name=_("Course content"))
    date_submitted = models.DateField(_("date submitted"),auto_now_add=True)
    
    #~ """Empty means 'any provider'
    #~ """
    #~ provider = models.ForeignKey(CourseProvider,blank=True,null=True,
        #~ verbose_name=_("Course provider"))
        
    #~ @chooser()
    #~ def provider_choices(cls):
        #~ return CourseProviders.request().queryset
        
    """
    when not empty,
    means that the request is satisfied and the Person participated to this course
    """
    course = models.ForeignKey("dsbe.Course",blank=True,null=True,
        verbose_name=_("Course found"))
        
    #~ """
    #~ The person's feedback about how satisfied she was.
    #~ """
    #~ satisfied = fields.StrengthField(verbose_name=_("Satisfied"),blank=True,null=True)
    
    remark = models.CharField(max_length=200,
        blank=True,null=True,
        verbose_name=_("Remark"))
        
    """Effective end of the course.
    """
    date_ended = models.DateField(blank=True,null=True,verbose_name=_("date ended"))
    
    """Person's feedback about this course.
    """
    ending = models.ForeignKey("dsbe.CourseEnding",blank=True,null=True,
        verbose_name=_("Ending"))
        
        
class Courses(reports.Report):
    model = Course
    order_by = ['start_date']

class CourseContents(reports.Report):
    model = CourseContent
    order_by = ['name']

class CoursesByProvider(Courses):
    fk_name = 'provider'

class CourseRequests(reports.Report):
    model = CourseRequest
    order_by = ['date_submitted']

class CourseRequestsByPerson(CourseRequests):
    fk_name = 'person'
    column_names = '* id'

class RequestsByCourse(CourseRequests):
    fk_name = 'course'
    label = _("Participants")
    can_add = perms.never

class CandidatesByCourse(CourseRequests):
    fk_name = 'course'
    label = _("Candidates")
    can_add = perms.never
    
    

#
# SEARCH
#
class PersonSearch(mixins.Printable):
    pass
    
  

"""
Here we add a new field `contract_type` to the 
standard model CompanyType.
http://osdir.com/ml/django-users/2009-11/msg00696.html
"""
from lino.modlib.contacts.models import CompanyType
CompanyType.add_to_class('contract_type',
    models.ForeignKey("dsbe.ContractType",
        blank=True,null=True,
        verbose_name=_("contract type")))
"""
Same for SiteConfig
"""
from lino.models import SiteConfig
SiteConfig.add_to_class('job_office',
    models.ForeignKey("contacts.Company",
        blank=True,null=True,
        verbose_name=_("Local job office"),
        related_name='job_office_sites',
        ))
resolve_field('lino.SiteConfig.job_office').__doc__ = """
The Company whose contact persons will be choices for `Person.job_office_contact`.
"""

"""
Here's how to override the default verbose_name of a field
"""
resolve_field('dsbe.Contract.user').verbose_name=_("responsible (DSBE)")

"""
...
"""
from lino.tools import resolve_model
User = resolve_model('auth.User')
User.grid_search_field = 'username'


"""
Here is how we install case-insensitive sorting in sqlite3.
Note that this caused noticeable performance degradation...

Thanks to 
- http://efreedom.com/Question/1-3763838/Sort-Order-SQLite3-Umlauts
- http://docs.python.org/library/sqlite3.html#sqlite3.Connection.create_collation
- http://www.sqlite.org/lang_createindex.html
"""
from django.db.backends.sqlite3.base import DatabaseWrapper
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
    if sender is DatabaseWrapper:
        db = kw['connection']
        db.connection.create_collation('BINARY', stricmp)

connection_created.connect(my_callback)
