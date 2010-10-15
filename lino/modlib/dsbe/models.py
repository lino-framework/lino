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

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import lino
#~ lino.log.debug(__file__+' : started')

from lino import reports
#~ from lino import layouts
from lino.utils import perms
from lino.utils import mixins
from lino import fields
from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
from lino.modlib.links import models as links
from lino.models import get_site_config
from lino.tools import get_field

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


#~ class PersonPicture(Action)
class Contact(contacts.Contact):
    
    class Meta:
        app_label = 'contacts'
        abstract = True
  
    id = models.AutoField(primary_key=True,verbose_name=_("ID"))
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
        r = super(Contact,self).save(*args,**kw)
        return r
        
    def before_save(self):
        if self.id is None:
            sc = get_site_config()
            if sc.next_partner_id is not None:
                self.id = sc.next_partner_id
                sc.next_partner_id += 1
                sc.save()
        
#~ class Person(Contact):

class Person(Contact,mixins.Printable):
    """
    Overrides :class:`contacts.Person`.
    """
    class Meta:
        app_label = 'contacts'
        
    first_name = models.CharField(max_length=200,blank=True,verbose_name=_('First name'))
    last_name = models.CharField(max_length=200,blank=True,verbose_name=_('Last name'))
    title = models.CharField(max_length=200,blank=True,verbose_name=_('Title'))
        
    def before_save(self):
        l = filter(lambda x:x,[self.last_name,self.first_name,self.title])
        self.name = " ".join(l)
        super(Person,self).before_save()
        
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
    birth_place = models.CharField(max_length=200,
        blank=True,null=True,
        verbose_name=("Birth place"))
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
    is_illiterate.return_type = models.BooleanField(verbose_name=_("illiterate"))
    
    def language_knowledge(self):
        l = []
        for kn in self.languageknowledge_set.all():
            if kn.spoken > '1' and kn.written > '1':
                l.append(_(u"%s (s/w)") % kn.language)
            elif kn.spoken > '1':
                l.append(_(u"%s (s)")% kn.language)
            elif kn.written > '1':
                l.append(_(u"%s (w)")% kn.language)
        return u", ".join(l)
    language_knowledge.return_type = models.TextField(verbose_name=_("Language knowledge"))
    
    def links_by_owner(self):
        s = ', '.join([u'<a href="%s">%s</a>' % (lnk.url,lnk.name) for lnk in links.LinksByOwner.request(master_instance=self)])
        return s
    #~ links_by_owner.return_type = models.TextField(verbose_name=_("Links"))
    links_by_owner.return_type = fields.HtmlBox(verbose_name=_("Links"))
    


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
    column_names = "name city links_by_owner * language_knowledge"
    #~ column_names = "name  city * language_knowledge"
    #~ column_names = "name city dsbe.LanguageKnowledgesByPerson" # dsbe.StudiesByPerson dsbe.ExclusionsByPerson"

    
    def disabled_fields(self,request,obj):
        if settings.DSBE_IS_IMPORTED_PARTNER(obj):
            return PERSON_TIM_FIELDS
        return []
        
class PersonsByNationality(Persons):
    app_label = 'contacts'
    fk_name = 'nationality'
    order_by = "city addr1"
    column_names = "city addr1 name country language"



#~ class Persons2(contacts.Persons):
    #~ pass
              
#~ class Company(Contact,contacts.Company):
class Company(Contact):
    class Meta:
        app_label = 'contacts'
    vat_id = models.CharField(max_length=200,blank=True)
    type = models.ForeignKey('contacts.CompanyType',blank=True,null=True,verbose_name=_("Company type"))
    #~ tim_nr = models.CharField(max_length=10,blank=True,null=True,unique=True,
        #~ verbose_name=_("TIM ID"))
    # PAR->Allo geht nach Person.title oder Company.prefix
    prefix = models.CharField(max_length=200,blank=True) 
    
    
COMPANY_TIM_FIELDS = [get_field(Company,n) for n in 
    '''name zip_code city country street 
    street_no street_box language 
    phone gsm fax email 
    bank_account1 bank_account2 activity'''.split()]
  
class Companies(contacts.Companies):
    app_label = 'contacts'
    #~ page_layouts = (CompanyDetail,)
    
    def disabled_fields(self,request,obj):
        if settings.DSBE_IS_IMPORTED_PARTNER(obj):
            return COMPANY_TIM_FIELDS
        return []
    
from lino.modlib.contacts.models import Companies



#
# PROJECT TYPE
# 

#~ class ProjectType(projects.ProjectType):
    #~ class Meta:
        #~ app_label = 'projects'

#~ class ProjectTypes(projects.ProjectTypes):
    #~ pass


#
# PROJECT
# 

#~ class Project(projects.Project):
  
    #~ person = models.ForeignKey("contacts.Person",blank=True,null=True,verbose_name=_("Person"))
    #~ company = models.ForeignKey("contacts.Company",blank=True,null=True,verbose_name=_("Company"))
    #~ why_stopped = models.CharField(max_length=200,blank=True,null=True,verbose_name=_("why stopped"))
    
    #~ class Meta:
        #~ app_label = 'projects'
        
        
#~ class ProjectDetail(projects.ProjectDetail):
    #~ main = """
    #~ name:40 type:20
    #~ started stopped why_stopped
    #~ person company
    #~ text:60
    #~ """
        

#~ class Projects(projects.Projects):
    #~ can_view = perms.is_authenticated
    #~ column_names = "name type person company *"
    #~ order_by = "name"
    
#~ class ProjectsByPerson(Projects):
    #~ label = _("Projects by Person")
    #~ fk_name = 'person'
    #~ order_by = "started"

#~ class ProjectsByCompany(Projects):
    #~ label = _("Projects by Company")
    #~ fk_name = 'company'
    #~ order_by = "started"
    
    
#
# STUDY TYPE
#
class StudyType(models.Model):
    name = models.CharField(max_length=200,verbose_name=_("Designation"))
    #~ text = models.TextField(blank=True,null=True,verbose_name=_("Description"))
    def __unicode__(self):
        return self.name

class StudyTypes(reports.Report):
    label = _('Study types')
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
    label = _("Studies & experiences")
    button_label = _("Studies")
    order_by = "started"
    
    
#
# LanguageKnowledge
#

class LanguageKnowledge(models.Model):
    person = models.ForeignKey("contacts.Person")
    #~ language = models.ForeignKey("countries.Language")
    language = fields.LanguageField()
    spoken = fields.KnowledgeField(verbose_name=_("spoken"))
    written = fields.KnowledgeField(verbose_name=_("written"))
    
class LanguageKnowledgesByPerson(reports.Report):
    model = LanguageKnowledge
    fk_name = 'person'
    label = _("Language knowledge")
    button_label = _("Languages")
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
    name = models.CharField(max_length=20)
    lst104 = models.BooleanField(verbose_name=_("Appears in Listing 104"))
    
    def __unicode__(self):
        return unicode(self.name)

class Activities(reports.Report):
    model = Activity
    label = _('Activities')

#~ class ActivitiesByPerson(Activities):
    #~ fk_name = 'activity'

#~ class ActivitiesByCompany(Activities):
    #~ fk_name = 'activity'
    
#
# EXCLUSION TYPES (Sperrgründe)
#
class ExclusionType(models.Model):
    name = models.CharField(max_length=20)
    
    def __unicode__(self):
        return unicode(self.name)

class ExclusionTypes(reports.Report):
    model = ExclusionType
    label = _('Exclusion Types')
    
#
# EXCLUSIONS (Arbeitslosengeld-Sperrungen)
#
class Exclusion(models.Model):
    person = models.ForeignKey("contacts.Person")
    type = models.ForeignKey("dsbe.ExclusionType",verbose_name=_("Reason"))
    excluded_from = models.DateField(blank=True,null=True,verbose_name=_("from"))
    excluded_until = models.DateField(blank=True,null=True,verbose_name=_("until"))
    remark = models.CharField(max_length=200,verbose_name=_("Remark"))
    
    def __unicode__(self):
        s = unicode(self.type)
        if self.excluded_from: s += ' ' +unicode(self.excluded_from)
        if self.excluded_until: s += '-'+unicode(self.excluded_until)
        return s

class Exclusions(reports.Report):
    model = Exclusion
    label = _('Exclusions')
    
class ExclusionsByPerson(Exclusions):
    fk_name = 'person'
    column_names = 'excluded_from excluded_until type remark'


#
# COACHING TYPES 
#
class CoachingType(models.Model):
    name = models.CharField(max_length=20)
    
    def __unicode__(self):
        return unicode(self.name)

class CoachingTypes(reports.Report):
    model = CoachingType
    label = _('Coaching Types')
    
#
# COACHINGS
#
class Coaching(models.Model):
    person = models.ForeignKey("contacts.Person",verbose_name=_("Client"))
    coach = models.ForeignKey("auth.User",verbose_name=_("Coach"))
    type = models.ForeignKey("dsbe.CoachingType",verbose_name=_("Coaching type"))
    remark = models.CharField(max_length=200,verbose_name=_("Remark"))
    

class Coachings(reports.Report):
    model = Coaching
    label = _('Coaches')
    
class CoachingsByPerson(Coachings):
    fk_name = 'person'
    column_names = 'coach type remark'

