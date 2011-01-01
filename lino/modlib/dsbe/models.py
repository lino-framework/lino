#coding: UTF-8
## Copyright 2008-2010 Luc Saffre
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

import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
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
from lino.models import get_site_config
from lino.tools import get_field
from lino.utils.babel import add_babel_field, default_language, babelattr
from lino.utils.choosers import chooser

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
]

# http://en.wikipedia.org/wiki/European_driving_licence

DRIVING_LICENSE_CHOICES = (
  ('A'  , _("Motorcycles") ),
  ('B'  , _("Car") ), # Auto
  ('C'  , _("Lorry") ),
  ('CE' , _("Lorry with trailer") ), 
  ('D'  , _("Bus") ), 
)

RESIDENCE_TYPE_CHOICES = (
  (1  , _("Registry of citizens")   ), # Bevölkerungsregister   registre de la population
  (2  , _("Registry of foreigners") ), # Fremdenregister        Registre des étrangers      vreemdelingenregister 
  (3  , _("Waiting for registry")   ), # Warteregister
)




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
          



#~ class Person(Contact):

class Person(Partner,contacts.Person):
#~ class Person(Partner,contacts.Person,mixins.Printable):
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
    is_dsbe = models.BooleanField(verbose_name=_("is coached"),default=False)
    #~ "Indicates whether this is coached."
    
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
    #~ driving_license = models.ForeignKey("dsbe.DrivingLicense",blank=True,null=True,
        #~ verbose_name=_("Driving license"))
    driving_license = models.CharField(max_length=4,blank=True,null=True,
        verbose_name=_("Driving license"),choices=DRIVING_LICENSE_CHOICES)
    
    no_shift = models.BooleanField(verbose_name=_("no shift work"))
    no_weekend = models.BooleanField(verbose_name=_("no work on week-end"))
    has_own_car = models.BooleanField(verbose_name=_("has own car"))
    #~ can_truck = models.BooleanField(verbose_name=_("Truck driving license"))
    can_clark = models.BooleanField(verbose_name=_("Clark driving license"))
    #~ can_bus = models.BooleanField(verbose_name=_("Bus driving license"))
    has_family = models.BooleanField(verbose_name=_("Head of a family"))
    
    it_knowledge = fields.KnowledgeField(blank=True,null=True,
        verbose_name=_("IT knowledge"))
        
    residence_permit_until = models.DateField(blank=True,null=True,verbose_name=_("Residence permit valid until"))
    residence_type = models.SmallIntegerField(blank=True,null=True,
        verbose_name=_("Residence type"),
        choices=RESIDENCE_TYPE_CHOICES,
        max_length=1,
        #~ limit_to_choices=True,
        )
    unemployed_since = models.DateField(blank=True,null=True,verbose_name=_("Unemployed since"))
    #~ work_permit_exempt = models.BooleanField(verbose_name=_("Work permit exemption"))
    needs_work_permit = models.BooleanField(verbose_name=_("Needs work permit"))
    work_permit_valid_until = models.DateField(blank=True,null=True,verbose_name=_("Work permit valid until"))
    work_permit_suspended_until = models.DateField(blank=True,null=True,verbose_name=_("suspended until"))
    aid_type = models.ForeignKey("dsbe.AidType",blank=True,null=True,
        verbose_name=_("aid type"))
    
    
    physical_handicap = models.BooleanField(verbose_name=_("Physical handicap"))
    mental_handicap = models.BooleanField(verbose_name=_("Mental handicap"))
    psycho_handicap = models.BooleanField(verbose_name=_("Psychological handicap"))
    health_problems = models.BooleanField(verbose_name=_("Health problems"))
    juristic_problems = models.BooleanField(verbose_name=_("Juristic problems"))
    dependency_problems = models.BooleanField(verbose_name=_("Dependency problems"))
    social_competence = models.BooleanField(verbose_name=_("Lack of social competence"))
    motivation_lack = models.BooleanField(verbose_name=_("Lack of motivation"))
    
    #~ unavailable = models.BooleanField(verbose_name=_("Unavailable"))
    unavailable_until = models.DateField(blank=True,null=True,verbose_name=_("Unavailable until"))
    unavailable_why = models.CharField(max_length=100,blank=True,null=True,verbose_name=_("reason"))
    
    fulltime_only = models.BooleanField(verbose_name=_("Fulltime only"))
    parttime_only = models.BooleanField(verbose_name=_("Part-time only"))
    young_children = models.BooleanField(verbose_name=_("Young children"))
    native_language = models.CharField(max_length=100,
        blank=True,null=True,
        verbose_name=_("Native language"))
    migration = models.BooleanField(verbose_name=_("Migration"))
    
        
    
    #~ def picture(self):
        #~ if self.national_id:
            #~ return "/images/" + self.national_id + ".jpg"
    #~ picture.return_type = models.ImageField() # fields.DataView('<img src=/>')
    
    #~ def get_target_parts(self,pm):
        #~ if isinstance(pm,mixins.PicturePrintMethod):
            #~ if self.card_number:
                #~ return [ "beid", self.card_number+".jpg" ]
            #~ return [ "pictures", "contacts.Person.jpg" ]
        #~ return mixins.Printable.get_target_parts(self,pm)
        
    def get_image_url(self,action):
        if self.card_number:
            return "beid/"+ self.card_number+".jpg"
        return "pictures/contacts.Person.jpg"
        
    
    #~ def image_url(self):
        #~ if self.card_number:
            #~ return "/media/beid/" + self.card_number + ".jpg"
            
    def is_illiterate(self):
        if self.languageknowledge_set.count() == 0:
            return False
        for lk in self.languageknowledge_set.all():
            if lk.written > 0:
                return False
        return True
    is_illiterate.return_type = models.BooleanField(verbose_name=_("Illiterate"))
    
    def overview(self):
        
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
    overview.return_type = fields.HtmlBox(verbose_name=_("Overview"))
    
    
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
    label = _("My coached Persons")
    order_by = ['last_name','first_name']
    #~ def get_queryset(self):
    def get_request_queryset(self,rr):
        q1 = models.Q(coach1__exact=rr.user)
        q2 = models.Q(coach2__exact=rr.user)
        #~ q2 = Q(coached__gt=0)
        #~ q2 = Q(dsbe_coach__exact=user)
        #~ q2 = Q(dsbe_coaches__contains=user)
        #~ q2 = Q(coaching_set__user__exact=user)
        #~ return Person.objects.annotate(dsbe_ccoach=Count('coaching_set__user__exact')).filter(q1|q2)
        return Person.objects.filter(q1|q2)
    #~ Person.user == user 
    #~ or 
    #~ Person.coachings_set.filter(user__exact=user).count() > 0        
    
              
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
        verbose_name = _("study or experience")
        verbose_name_plural = _("Studies & experiences")
    person = models.ForeignKey("contacts.Person",verbose_name=_("Person"))
    type = models.ForeignKey(StudyType,verbose_name=_("Study type"))
    content = models.CharField(max_length=200,blank=True,null=True,verbose_name=_("Study content"))
    #~ content = models.ForeignKey(StudyContent,blank=True,null=True,verbose_name=_("Study content"))
  
    started = fields.MonthField(blank=True,null=True,verbose_name=_("started"))
    stopped = fields.MonthField(blank=True,null=True,verbose_name=_("stopped"))
    success = models.BooleanField(verbose_name=_("Success"),default=True)
    country = models.ForeignKey("countries.Country",blank=True,null=True,verbose_name=_("Country"))
    #~ language = models.ForeignKey("countries.Language",blank=True,null=True,verbose_name=_("Language"))
    language = fields.LanguageField(blank=True,null=True,verbose_name=_("Language"))
    
    school = models.CharField(max_length=200,blank=True,null=True,verbose_name=_("School"))
    #~ school = models.ForeignKey("contacts.Company",blank=True,null=True,verbose_name=_("School"))
    
    remarks = models.TextField(blank=True,null=True,verbose_name=_("Remarks"))
    
    def __unicode__(self):
        return unicode(self.type)
  
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
    #~ language = models.ForeignKey("countries.Language")
    language = fields.LanguageField()
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
# DRIVING LICENSE
#
#~ class DrivingLicense(models.Model):
    #~ id = models.CharField(max_length=4,primary_key=True,verbose_name=_("Code"))
    #~ name = models.CharField(max_length=40)
    
    #~ def __unicode__(self):
        #~ return u'%s (%s)' % (self.id,self.name)

#~ class DrivingLicenses(reports.Report):
    #~ model = DrivingLicense
    #~ label = _('Driving licenses')

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
    
    applies_from = models.DateField(blank=True,null=True,verbose_name=_("applies from"))
    applies_until = models.DateField(blank=True,null=True,verbose_name=_("applies until"))
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
  

"""
http://osdir.com/ml/django-users/2009-11/msg00696.html
"""
from lino.modlib.contacts.models import CompanyType

CompanyType.add_to_class('contract_type',
    models.ForeignKey("dsbe.ContractType",
        blank=True,null=True,
        verbose_name=_("contract type")))

"""
here's how to override the default verbose_name of a field
"""
from lino.tools import resolve_field
resolve_field('dsbe.Contract.user').verbose_name=_("responsible (DSBE)")

from lino.tools import resolve_model
User = resolve_model('auth.User')
User.grid_search_field = 'username'


"""
Here is how to install case-insensitive sorting in sqlite.

Thanks to 
- http://efreedom.com/Question/1-3763838/Sort-Order-SQLite3-Umlauts
- http://docs.python.org/library/sqlite3.html#sqlite3.Connection.create_collation
- http://www.sqlite.org/lang_createindex.html
"""
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.backends.signals import connection_created

def german(s):
  
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
    return cmp(german(str1),german(str2))
    
def my_callback(sender,**kw):
    if sender is DatabaseWrapper:
        db = kw['connection']
        db.connection.create_collation('BINARY', stricmp)

connection_created.connect(my_callback)
