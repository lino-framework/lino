# -*- coding: UTF-8 -*-
## Copyright 2008-2011 Luc Saffre
## This file is part of the Lino-DSBE project.
## Lino-DSBE is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-DSBE is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-DSBE; if not, see <http://www.gnu.org/licenses/>.

import decimal
from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
#~ from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _


from lino.utils import i2d
from lino.utils.instantiator import Instantiator
from lino.tools import resolve_model
from lino.utils.babel import babel_values, default_language
from lino.utils.restify import restify
from lino.utils import dblogger
from lino.models import update_site_config
from lino.utils import mti

#~ from django.contrib.auth import models as auth
from lino.modlib.users import models as auth
from lino.modlib.contacts.models import SEX_FEMALE, SEX_MALE

#~ dblogger.info('Loading')

DEMO_LINKS = [
  dict(name="Lino website",url="http://lino.saffre-rumma.net"),
  dict(name="Django website",url="http://www.djangoproject.com"),
  dict(name="ExtJS website",url="http://www.sencha.com"),
  dict(name="Python website",url="http://www.python.org"),
  dict(name="Google",url="http://www.google.com"),
]
ROW_COUNTER = 0
MAX_LINKS_PER_OWNER = 4
DATE = i2d(20061014)
    


#~ auth = models.get_app('auth')
#~ projects = models.get_app('projects')
#~ contacts = models.get_app('contacts')
#~ notes = models.get_app('notes')
#~ properties = models.get_app('properties')


#char_pv = Instantiator('properties.CharPropValue').build
#CharPropValue = resolve_model('properties.CharPropValue')
#~ from lino.modlib.properties import models as properties # CharPropValue, BooleanPropValue
#~ CHAR = ContentType.objects.get_for_model(properties.CharPropValue)
#BOOL = ContentType.objects.get_for_model(properties.BooleanPropValue)
#~ INT = ContentType.objects.get_for_model(properties.IntegerPropValue)

#~ def fill_choices(p,model):
    #~ i = 0
    #~ choices = p.choices_list()
    #~ if len(choices) == 0:
        #~ return
    #~ for owner in model.objects.all():
        #~ p.set_value_for(owner,choices[i])
        #~ if i + 1 < len(choices): 
            #~ i += 1
        #~ else:
            #~ i = 0

#~ StudyContent = resolve_model('dsbe.StudyContent')



def objects():
  
    Person = resolve_model('contacts.Person')
    Company = resolve_model('contacts.Company')
    Contact = resolve_model('contacts.Contact')
    Contract = resolve_model('jobs.Contract')
    JobProvider = resolve_model('jobs.JobProvider')
    Note = resolve_model('notes.Note')
    User = resolve_model('users.User')
    Country = resolve_model('countries.Country')

    person = Instantiator(Person).build
    company = Instantiator(Company).build
    contact = Instantiator(Contact).build
    exam_policy = Instantiator('jobs.ExamPolicy').build

    City = resolve_model('countries.City')
    StudyType = resolve_model('dsbe.StudyType')
    Country = resolve_model('countries.Country')
    Property = resolve_model('properties.Property')
  
    
    #~ country = Instantiator('countries.Country',"isocode name").build
    #~ yield country('SUHH',"Soviet Union")
    
    eupen = City.objects.get(name__exact='Eupen')
    kettenis = City.objects.get(name__exact='Kettenis')
    vigala = City.objects.get(name__exact='Vigala')
    ee = Country.objects.get(pk='EE')
    be = Country.objects.get(isocode__exact='BE')
    #~ luc = person(first_name="Luc",last_name="Saffre",city=vigala,country='EE',card_number='122')
    #~ yield luc
    andreas = Person.objects.get(name__exact="Arens Andreas")
    annette = Person.objects.get(name__exact="Arens Annette")
    hans = Person.objects.get(name__exact="Altenberg Hans")
    
    cpas = company(name=u"ÖSHZ Eupen",city=eupen,country='BE')
    yield cpas
    bisa = company(name=u"BISA",city=eupen,country='BE')
    yield bisa 
    bisa_dir = contact(company=bisa,person=annette,type=1)
    yield bisa_dir 
    rcycle = company(name=u"R-Cycle Sperrgutsortierzentrum",city=eupen,country='BE')
    yield rcycle
    rcycle_dir = contact(company=rcycle,person=andreas,type=1)
    yield rcycle_dir
    yield company(name=u"Die neue Alternative V.o.G.",city=eupen,country='BE')
    yield company(name=u"Pro Aktiv V.o.G.",city=eupen,country='BE')
    yield company(name=u"Werkstatt Cardijn V.o.G.",city=eupen,country='BE')
    yield company(name=u"Behindertenstätten Eupen",city=eupen,country='BE')
    yield company(name=u"Beschützende Werkstätte Eupen",city=eupen,country='BE')
    
    luc = Person.objects.get(name__exact="Saffre Luc")
    luc.birth_place = 'Eupen'
    luc.birth_country = be
    luc.save()
    ly = person(first_name="Ly",last_name="Rumma",
      city=vigala,country='EE',card_number='123',birth_country=ee,
      birth_date=i2d(19680101),birth_date_circa=True,sex='F')
    yield ly
    mari = person(first_name="Mari",last_name="Saffre",
      city=vigala,country='EE',card_number='124',birth_country=ee,birth_date=i2d(20020405),sex='F')
    yield mari
    iiris = person(first_name="Iiris",last_name="Saffre",
      city=vigala,country='EE',card_number='125',birth_country=ee,birth_date=i2d(20080324),sex='F')
    yield iiris
    
    gerd = person(first_name="Gerd",last_name="Xhonneux",city=kettenis,name="Xhonneux Gerd",country='BE',sex='M')
    yield gerd
    yield contact(company=cpas,person=gerd,type=4)
    
    
    tatjana = person(first_name=u"Татьяна",last_name=u"Казеннова",# name="Казеннова Татьяна",
        city=kettenis,country='BE', 
        birth_place="Moskau", # birth_country='SUHH',
        sex='F')
    yield tatjana
    
    from django.core.exceptions import ValidationError
    # a circular reference: bernard is contact for company adg and also has himself as `job_office_contact`
    bernard = Person.objects.get(name__exact="Bodard Bernard")
    adg = company(name=u"Arbeitsamt der D.G.",city=eupen,country='BE')
    update_site_config(job_office=adg)
    yield adg
    adg_dir = contact(company=adg,person=bernard,type=1)
    yield adg_dir
    try:
      bernard.job_office_contact = adg_dir
      bernard.clean()
      #~ bernard.save()
    except ValidationError:
        pass
    else:
        raise Exception("Expected ValidationError")
      
    
    
    
    #~ oshz = Company.objects.get(name=u"ÖSHZ Eupen")
    
    
    #~ project = Instantiator('projects.Project').build
    note = Instantiator('notes.Note').build
    langk = Instantiator('dsbe.LanguageKnowledge').build

    user = auth.User.objects.get(username='user')
    root = auth.User.objects.get(username='root')
    
    #~ prj = project(name="Testprojekt",company=oshz)
    #~ yield prj 
    #~ yield note(user=user,project=prj,date=i2d(20091006),subject="Programmierung",company=oshz)
    
    #~ prj = project(name="Testprojekt",company=oshz)
    #~ yield prj 
    #~ yield note(user=user,project=prj,date=i2d(20091007),subject="Anschauen",company=oshz)
    
    
    yield note(user=root,date=i2d(20091006),
        subject="Programmierung",company=cpas,
        type=1,event_type=1)
    yield note(user=user,date=i2d(20091007),subject="Testen",company=cpas)
    yield note(user=root,date=i2d(20100517),subject="Programmierung",company=cpas)
    yield note(user=user,date=i2d(20100518),subject="Testen",company=cpas)
    yield note(user=user,date=i2d(20110526),subject="Formatted notes",
        company=cpas,body=restify(u"""\
Formatted notes
===============

Lino has now a WYSIWYG text editor. 

Examples
--------

- Enumerations like this list
- Character formatting : **bold**, *italics*, ``typewriter``.
- External `Links <http://lino.saffre-rumma.net/todo.html>`_
- Tables:

  ============ =======
  Package      Version
  ============ =======
  mercurial    1
  apache2      2 
  tinymce      3
  ============ =======
  
Lorem ipsum 
-----------

Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.  

"""))
    
    schule = StudyType.objects.get(pk=1)
    uni = StudyType.objects.get(pk=4)
    #~ abi = StudyContent.objects.get(name=u"Abitur")
    abi = u"Abitur"
    study = Instantiator('dsbe.Study').build
        
    yield study(person=luc,type=schule,content=abi,started='19740901',stopped='19860630')
    yield study(person=gerd,type=schule,content=abi,started='19740901',stopped='19860630')

    yield langk(person=luc,language='ger',written='4',spoken='4')
    yield langk(person=gerd,language='ger',written='4',spoken='4')
    yield langk(person=mari,language='ger',written='2',spoken='4')
    yield langk(person=iiris,language='ger',written='0',spoken='4')
    yield langk(person=ly,language='ger',written='2',spoken='1')
    
    yield langk(person=luc,language='fre',written='4',spoken='3')
    yield langk(person=gerd,language='fre',written='4',spoken='3')
    
    yield langk(person=luc,language='eng',written='4',spoken='3')
    yield langk(person=gerd,language='eng',written='4',spoken='3')
    yield langk(person=ly,language='eng',written='3',spoken='3')
    
    yield langk(person=gerd,language='dut',written='3',spoken='3')
    
    yield langk(person=luc,language='est',written='3',spoken='3')
    yield langk(person=ly,language='est',written='4',spoken='4')
    yield langk(person=mari,language='est',written='3',spoken='4')
    yield langk(person=iiris,language='est',written='0',spoken='3')
    
    
    jobtype = Instantiator('jobs.JobType','name').build
    art607 = jobtype(u'Sozialwirtschaft = "majorés"')
    yield art607 
    yield jobtype(u'INTERN')
    yield jobtype(u'EXTERN (Öffentl. VoE mit Kostenrückerstattung)')
    yield jobtype(u'EXTERN (Privat Kostenrückerstattung)')
    yield jobtype(u'VSE')
    yield jobtype(u'Sonstige (alle nicht')
    
    rcycle = mti.insert_child(rcycle,JobProvider)
    yield rcycle 
    bisa = mti.insert_child(bisa,JobProvider)
    yield bisa 
    
    job = Instantiator('jobs.Job','provider type contract_type name').build
    bisajob = job(bisa,art607,1,"bisa")
    yield bisajob
    rcyclejob = job(rcycle,art607,2,"rcycle")
    yield rcyclejob 
    contract = Instantiator('jobs.Contract',
      'type applies_from applies_until job contact',
      user=root,person=hans).build
    yield contract(1,i2d(20090518),i2d(20090517),rcyclejob,rcycle_dir)
    yield contract(1,i2d(20100518),i2d(20100517),bisajob,bisa_dir)
    yield contract(1,None,None,bisajob,bisa_dir,person=tatjana)
    yield contract(1,i2d(20110601),None,bisajob,bisa_dir,person=andreas)
    yield contract(1,i2d(20110601),None,rcyclejob,rcycle_dir,person=annette)
    
    jobrequest = Instantiator('jobs.JobRequest','job person').build
    yield jobrequest(bisajob,tatjana)
    yield jobrequest(rcyclejob,luc)

    #~ def f(rmd,d):
        #~ rmd.reminder_date = d
        #~ rmd.reminder_text = 'demo reminder'
        #~ rmd.save()
        
    #~ for rmd in Note.objects.all(): f(rmd,i2d(20101110))
    #~ for rmd in Contract.objects.all(): f(rmd,i2d(20101111))
      
      
      
    
    link = Instantiator('links.Link').build
    
    users = User.objects.all()
    
    
    def demo_links(**kw):
        global ROW_COUNTER
        global DATE
        for x in range(1 + (ROW_COUNTER % MAX_LINKS_PER_OWNER)):
            kw.update(date=DATE)
            kw.update(DEMO_LINKS[ROW_COUNTER % len(DEMO_LINKS)])
            kw.update(user=users[ROW_COUNTER % users.count()])
            DATE += ONE_DAY
            ROW_COUNTER += 1
            yield link(**kw)
      
    for obj in Person.objects.all():
        for x in demo_links(person=obj):
            yield x
            
    for obj in Company.objects.all():
        for x in demo_links(company=obj):
            yield x
            
    

    #~ from lino.sites.dsbe.models import Course, CourseContent, CourseRequest
    
    courseprovider = Instantiator('dsbe.CourseProvider').build
    #~ oikos = company(name=u"Oikos",city=eupen,country='BE',
      #~ is_courseprovider=True)
    oikos = courseprovider(name=u"Oikos",city=eupen,country='BE')
    yield oikos
    
    #~ kap = company(name=u"KAP",city=eupen,country='BE',
      #~ is_courseprovider=True)
    kap = courseprovider(name=u"KAP",city=eupen,country='BE')
    yield kap
    
    CourseContent = resolve_model('dsbe.CourseContent')
    yield CourseContent(id=1,name=u"Deutsch")
    yield CourseContent(id=2,name=u"Französisch")
    
    course = Instantiator('dsbe.Course').build
    yield course(provider=oikos,title=u"Deutsch für Anfänger",content=1,start_date=i2d(20110110))
    yield course(provider=kap,title=u"Deutsch fur Anfanger",content=1,start_date=i2d(20110117))
    yield course(provider=kap,title=u"Français pour débutants",content=2,start_date=i2d(20110124))
    
    #~ baker = Properties.objects.get(pk=1)
    #~ baker.save()
    #~ yield baker

    pp = Instantiator('properties.PersonProperty',
        'person property value').build
    for p in Person.objects.all():
        for prop in Property.objects.all():
            yield pp(p,prop,prop.type.default_value)
            
    langk = Instantiator('dsbe.LanguageKnowledge',
        'person:name language written spoken').build
    yield langk(u"Ausdemwald Alfons",'est','1','1')
    yield langk(u"Ausdemwald Alfons",'ger','4','3')
    yield langk(u"Bastiaensen Laurent",'ger','4','3')
    yield langk(u"Bastiaensen Laurent",'fre','4','3')
    yield langk(u"Eierschal Emil",'ger','4','3')
    yield langk(u"Ärgerlich Erna",'ger','4','4')
    
    for p in Person.objects.all():
        if p.zip_code == '4700':
            p.languageknowledge_set.create(language_id='ger',native=True)
            p.is_cpas = True
            p.is_active = True
            #~ p.native_language_id = 'ger'
            p.birth_country_id = 'BE'
            p.nationality_id = 'BE'
            p.save()

    for short_code,isocode in (
        ('B', 'BE'),
        ('D', 'DE'),
        ('F', 'FR'),
      ):
      c = Country.objects.get(pk=isocode)
      c.short_code = short_code
      c.save()
      
    p = Person.objects.get(name=u"Ärgerlich Erna")
    p.birth_date = i2d(19800301)
    p.coached_from = i2d(20100301)
    p.coached_until = None
    p.coach1 = User.objects.get(username='root')
    p.sex = SEX_FEMALE
    p.save()
    
    task = Instantiator('cal.Task').build
    yield task(user=root,start_date=i2d(20110717),summary=u"Anrufen Termin",
        owner=p)
    
    p = Person.objects.get(name=u"Eierschal Emil")
    p.birth_date = i2d(19800501)
    p.coached_from = i2d(20100801)
    p.coached_until = i2d(20101031)
    p.coach1 = User.objects.get(username='root')
    p.sex = SEX_MALE
    p.national_id = 'INVALID-45'
    p.save()

    p = Person.objects.get(name=u"Bastiaensen Laurent")
    p.birth_date = i2d(19810601)
    p.coached_from = None
    p.coached_until = i2d(20101031)
    p.unavailable_until = i2d(20110712)
    p.coach1 = User.objects.get(username='root')
    p.sex = SEX_MALE
    p.national_id = '931229 211-83'
    p.save()

    p = Person.objects.get(name=u"Ausdemwald Alfons")
    p.birth_date = i2d(19500301)
    p.coach1 = User.objects.get(username='root')
    p.sex = SEX_MALE
    p.save()

    persongroup = Instantiator('dsbe.PersonGroup','name').build
    yield persongroup(u"Bilan / Détermination Rémobilisation",ref_name='1')
    yield persongroup(u"Préformation",ref_name='2')
    yield persongroup(u"Formation",ref_name='3')
    yield persongroup(u"Recherche active emplois",ref_name='4')
    yield persongroup(u"Travail",ref_name='4bis')


    etype = Instantiator('cal.EventType','name').build
    yield etype("interner Termin")
    yield etype("Termin beim Klienten")
    yield etype("Termin beim Arbeitgeber")
    
    event = Instantiator('cal.Event',
      'type start_date person summary',
      user=root).build
    yield event(1,i2d(20100727),hans,u"Stand der Dinge")
    yield event(2,i2d(20100727),annette,u"Problem Kühlschrank")
    yield event(3,i2d(20100727),andreas,u"Mein dritter Termin")
