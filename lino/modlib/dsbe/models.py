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
**Overview**

  A :class:`Contact` is either a :class:`Person` or a :class:`Company`.

  The :class:`Activity` of a :class:`Person` or :class:`Company` 
  indicates in what professional area they are active.

  :class:`Coaching` is when a :class:`auth.User` has been designated responsible 
  for a :class:`Person`. There may be more than one responsible user per person, 
  each one having a different :class:`CoachingType`.

  For each :class:`Person` we keep a record of :class:`Exclusions <Exclusion>` 
  (each with an optional :class:`ExclusionType`).

  For each :class:`Person` we keep a record of her :class:`LanguageKnowledge`.

  ...

"""

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.encoding import force_unicode 

import lino
#~ lino.log.debug(__file__+' : started')

from lino import reports
#~ from lino import layouts
from lino.utils import perms
#~ from lino.utils import printable
from lino.utils import mixins
from lino import fields
from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
from lino.modlib.links import models as links
from lino.models import get_site_config
from lino.tools import get_field
from lino.tools import default_language

#~ from lino.modlib.fields import KNOWLEDGE_CHOICES # for makemessages

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


class Partner(models.Model):
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
        
#~ class Person(Contact):

class Person(Partner,contacts.Person,mixins.Printable):
    """
    Implements :class:`contacts.Person`, 
    but cannot inherit from :mod:`lino.modlib.contacts.models.Person`
    (see :doc:`/tickets/7`).
    
    This is also Printable just to demonstrate that not only Notes are printables.
    
    Inner class Meta is necessary because of :doc:`/tickets/14`.
    """
    
    class Meta(contacts.Person.Meta):
        #~ app_label = 'contacts'
        verbose_name = _("person")
        verbose_name_plural = _("persons")
        
    #~ first_name = models.CharField(max_length=200,blank=True,verbose_name=_('First name'))
    #~ last_name = models.CharField(max_length=200,blank=True,verbose_name=_('Last name'))
    #~ title = models.CharField(max_length=200,blank=True,verbose_name=_('Title'))
        
    def get_queryset(self):
        return self.model.objects.select_related('country','city','user','nationality')
        
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
    
    user = models.ForeignKey("auth.User",blank=True,null=True,
        verbose_name=_("User"))
        
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
    
    accepts_shift = models.BooleanField(verbose_name=_("ready to work in shifted time"))
    accepts_we = models.BooleanField(verbose_name=_("ready to work on week-end"))
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
    
    


PERSON_TIM_FIELDS = [get_field(Person,n) for n in 
    '''name first_name last_name title 
    zip_code city country street street_no street_box 
    birth_date sex birth_place user language 
    phone gsm fax email 
    card_number card_valid_from card_valid_until
    national_id health_insurance pharmacy 
    bank_account1 bank_account2 
    gesdos_id activity 
    is_cpas is_senior is_active nationality'''.split()]

class Persons(contacts.Persons):
    can_view = perms.is_authenticated
    app_label = 'contacts'
    #~ page_layouts = (PersonDetail,)
    #~ column_names = "name city dsbe.LanguageKnowledgesByPerson *"
    #~ column_names = "name city dsbe.LanguageKnowledgesByPerson *"
    #~ column_names = "name city links.LinksByOwner language_knowledge"
    #~ column_names = "name city dsbe.LanguageKnowledgesByPerson" # dsbe.StudiesByPerson dsbe.ExclusionsByPerson"

    
    def disabled_fields(self,request,obj):
        if settings.DSBE_IS_IMPORTED_PARTNER(obj):
            return PERSON_TIM_FIELDS
        return []
        
class PersonsByNationality(Persons):
    app_label = 'contacts'
    fk_name = 'nationality'
    order_by = "city name"
    column_names = "city addr1 name country language *"
    
class PersonsByCity(Persons):
    app_label = 'contacts'
    fk_name = 'city'
    order_by = 'addr1 street street_no street_box'
    column_names = "addr1 street street_no street_box name language *"

#~ class Persons2(contacts.Persons):
    #~ pass
              
#~ class Company(Contact,contacts.Company):
#~ class Company(Partner,contacts.Addressable,):
class Company(Partner,contacts.Company):
  
    """
    Implements :class:`contacts.Company`, 
    but cannot inherit from :mod:`lino.modlib.contacts.models.Company`
    (see :doc:`/tickets/7`).
    
    Inner class Meta is necessary because of :doc:`/tickets/14`.
    """
    
    class Meta(contacts.Company.Meta):
        #~ app_label = 'contacts'
        verbose_name = _("company")
        verbose_name_plural = _("companies")
    #~ vat_id = models.CharField(max_length=200,blank=True)
    #~ type = models.ForeignKey('contacts.CompanyType',blank=True,null=True,verbose_name=_("Company type"))
    prefix = models.CharField(max_length=200,blank=True) 
    
    
COMPANY_TIM_FIELDS = [get_field(Company,n) for n in 
    '''name zip_code city country street 
    street_no street_box language 
    phone gsm fax email 
    bank_account1 bank_account2 activity'''.split()]
  
class Companies(contacts.Companies):
    app_label = 'contacts'
    
    def disabled_fields(self,request,obj):
        if settings.DSBE_IS_IMPORTED_PARTNER(obj):
            return COMPANY_TIM_FIELDS
        return []
    
#~ from lino.modlib.contacts.models import Companies


    
#
# STUDY TYPE
#
class StudyType(models.Model):
    name = models.CharField(max_length=200,verbose_name=_("Designation"))
    #~ text = models.TextField(blank=True,null=True,verbose_name=_("Description"))
    class Meta:
        verbose_name = _("study type")
        verbose_name_plural = _("study types")
    def __unicode__(self):
        return self.name

class StudyTypes(reports.Report):
    #~ label = _('Study types')
    model = StudyType
    order_by = "name"

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
    order_by = "started"
    
    
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
    name = models.CharField(max_length=20)
    lst104 = models.BooleanField(verbose_name=_("Appears in Listing 104"))
    
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
class CoachingType(models.Model):
    class Meta:
        verbose_name = _("coaching type")
        verbose_name_plural = _('coaching types')
        
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return unicode(self.name)

class CoachingTypes(reports.Report):
    model = CoachingType
    #~ label = _('Coaching Types')
    
#
# COACHINGS
#
class Coaching(models.Model):
    class Meta:
        verbose_name = _("coaching")
        verbose_name_plural = _('coachings')
    person = models.ForeignKey("contacts.Person",verbose_name=_("Client"))
    coach = models.ForeignKey("auth.User",verbose_name=_("Coach"))
    type = models.ForeignKey("dsbe.CoachingType",verbose_name=_("Coaching type"))
    remark = models.CharField(max_length=200,blank=False,verbose_name=_("Remark"))
    

class Coachings(reports.Report):
    model = Coaching
    
class CoachingsByPerson(Coachings):
    fk_name = 'person'
    column_names = 'coach type remark *'
    label = _('Coaches')

#
# CONTRACT TYPES 
#
class ContractType(mixins.PrintableType):
    templates_group = 'contracts'
    class Meta:
        verbose_name = _("contract type")
        verbose_name_plural = _('contract types')
        
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return unicode(self.name)

class ContractTypes(reports.Report):
    model = ContractType
    column_names = 'name build_method template *'
    
#
# CONTRACTS
#
class Contract(mixins.TypedPrintable,mixins.AutoUser):
    class Meta:
        verbose_name = _("contract")
        verbose_name_plural = _('contracts')
        
    client = models.ForeignKey("contacts.Person",verbose_name=_("Client"))
    company = models.ForeignKey("contacts.Company",verbose_name=_("Company"))
    contact = models.ForeignKey("contacts.Contact",blank=True,null=True,
      verbose_name=_("represented by"))
    #~ user = models.ForeignKey("auth.User",verbose_name=_("Coach"))
    type = models.ForeignKey("dsbe.ContractType",verbose_name=_("Contract type"))
    applies_from = models.DateField(blank=True,null=True,verbose_name=_("applies from"))
    applies_until = models.DateField(blank=True,null=True,verbose_name=_("applies until"))
    language = fields.LanguageField(default=default_language)
    
    @classmethod
    def contact_choices(cls,company):
        if company is not None:
            return company.contact_set.all()
        return []
        #~ print 'Contract.contact_choices for', company
        #~ choices = company.contact_set.all()
        #~ print 'Contract.contact_choices returns', choices
        #~ return choices
    

class Contracts(reports.Report):
    model = Contract
    
class ContractsByPerson(Contracts):
    fk_name = 'client'
    column_names = 'company applies_from applies_until user type *'

class ContractsByCompany(Contracts):
    fk_name = 'company'
    column_names = 'client applies_from applies_until user type *'

class ContractsByType(Contracts):
    fk_name = 'type'
    column_names = "applies_from client company user *"
    order_by = "applies_from"
