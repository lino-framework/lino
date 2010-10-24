# -*- coding: UTF-8 -*-
## Copyright 2009-2010 Luc Saffre
## This file is part of the TimTools project.
## TimTools is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## TimTools is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with TimTools; if not, see <http://www.gnu.org/licenses/>.

"""

Performs a database reset and initial import of your TIM data. 
Mandatory argument is the path to your TIM data directory.

"""


import os
import sys
import datetime

from dateutil import parser as dateparser

from django.conf import settings
from django.core.management import call_command
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from lino import lino_site
from lino.utils import dbfreader
#~ from lino import diag

from lino.modlib.contacts.utils import name2kw, street2kw, join_words
from lino.utils.instantiator import Instantiator

from lino.tools import resolve_model, obj2str
import lino

from lino.utils import confirm, iif


Activity = resolve_model('dsbe.Activity')
Country = resolve_model('countries.Country')
City = resolve_model('countries.City')
Person = resolve_model('contacts.Person')
Company = resolve_model('contacts.Company')


def store(kw,**d):
    for k,v in d.items():
        #~ if v is not None:
        if v:
            kw[k] = v

def convert_username(name):
    return name.lower()
  
def convert_sex(v):
    if v in ('W','F'): return 'F'
    if v == 'M': return 'M'
    return None
      
def isolang(x):
    if x == 'K' : return 'et'
    if x == 'E' : return 'en'
    if x == 'D' : return 'de'
    if x == 'F' : return 'fr'
    if x == 'N' : return 'nl'
      
def is_company(data):
    # wer eine nationalregisternummer hat ist eine Person, selbst wenn er auch eine MWst-Nummer hat.
    if data.get('NB2',False):
        return False
    if data.get('NOTVA',False):
    #~ if data.get('NOTVA',False):
        return True
    return False
    
      
      
def ADR_id(cIdAdr):
    assert len(cIdAdr) == 3
    #~ assert [cIdAdr:-3] == '000'
    try:
        return 199000+int(cIdAdr)
    except ValueError,e:
        return None

      
      
def country2kw(row,kw):
    # for both PAR and ADR
    
    country = row['PAYS']
    if country:
        try:
            country = Country.objects.get(short_code__exact=country)
        except Country.DoesNotExist:
            country = Country(isocode=country,name=country,short_code=country)
            country.save()
    kw.update(country=country)
    
    store(kw,
      phone=row['TEL'],
      fax=row['FAX'],
      email=row['EMAIL'],
      )
    
    zip_code = row['CP']
    if zip_code:
        kw.update(zip_code=zip_code)
        try:
            city = City.objects.get(
              country=country,
              zip_code__exact=zip_code,
              )
            kw.update(city=city)
        except City.DoesNotExist,e:
            city = City(zip_code=zip_code,name=zip_code,country=country)
            city.save()
            kw.update(city=city)
            #~ lino.log.warning("%s-%s : %s",row['PAYS'],row['CP'],e)
        except City.MultipleObjectsReturned,e:
            lino.log.warning("%s-%s : %s",row['PAYS'],row['CP'],e)
      
def pxs2person(row,person):
  
    kw = {}
    store(kw,
      card_number=row['CARDNUMBER'],
      birth_place=row['BIRTHPLACE'],
      sex=convert_sex(row['SEXE'])
    )
    for k,v in kw.items():
        setattr(person,k,v)
        
    person.is_active = iif(row['IDPRT']=='I',False,True)
    if row['IDPRT'] == 'S':
        person.is_cpas = True
    elif row['IDPRT'] == 'A':
        person.is_senior = True
        
    if row['IDMUT']:
        try:
            person.health_insurance = Company.objects.get(pk=ADR_id(row['IDMUT']))
        except ValueError,e:
            lino.log.warning(u"%s : invalid health_insurance %r",person,row['IDMUT'])
        except Company.DoesNotExist,e:
            lino.log.warning(u"%s : health_insurance %s not found",person,row['IDMUT'])
            pass
  
    if row['APOTHEKE']:
        try:
            person.pharmacy = Company.objects.get(pk=int(row['APOTHEKE']))
        except ValueError,e:
            lino.log.warning(u"%s : invalid pharmacy %r",person,row['APOTHEKE'])
        except Company.DoesNotExist,e:
            lino.log.warning(u"%s : pharmacy %s not found",person,row['APOTHEKE'])
            
    nat = row['NATIONALIT']
    if nat:
        try:
            country = Country.objects.get(short_code__exact=nat)
        except Country.DoesNotExist:
            country = Country(isocode=nat,name=nat,short_code=nat)
            country.save()
        person.nationality=country
            
    if row['GEBDAT']:
        person.birth_date = dateparser.parse(row['GEBDAT'])
    if row['VALID1']:
        person.card_valid_from = dateparser.parse(row['VALID1'])
    if row['VALID2']:
        person.card_valid_until = dateparser.parse(row['VALID2'])
        
        
    
def load_dbf(dbpath,tableName,load):
    fn = os.path.join(dbpath,'%s.DBF' % tableName)
    f = dbfreader.DBFFile(fn,codepage="cp850")
    lino.log.info("Loading %d records from %s...",len(f),fn)
    f.open()
    for dbfrow in f:
        i = load(dbfrow)
        if i is not None:
            try:
                i.save()
                #~ lino.log.debug("%s has been saved",i)
            except ValidationError,e:
                lino.log.warning("Failed to save row %s from %s : %s",obj2str(i),dbfrow,e)
                lino.log.exception(e)
            except IntegrityError,e:
                lino.log.warning("Failed to save row %s from %s : %s",obj2str(i),dbfrow,e)
                lino.log.exception(e)
    f.close()

    
def unused_tim_fixture_objects():
    noteType = Instantiator('notes.NoteType','name print_method template').build
    yield noteType((u"Auswertungsbogen allgemein"),'appy',u'Auswertungsbogen_allgemein.odt')
    yield noteType((u"Anwesenheitsbescheinigung"),'appy',u'Anwesenheitsbescheinigung.odt')
    yield noteType((u"Beschluss"),'appy',u'Beschluss.odt')
    yield noteType((u"Konvention"),'appy',u'Konvention.odt')
    yield noteType((u"Brief"),'appy',u'Brief.odt')
    yield noteType((u"Vorladung"),'appy',u'Vorladung.odt')
    yield noteType((u"VSE Lehre"),'appy',u'VSE Lehre.odt')
    yield noteType((u"VSE Ausbildung"),'appy',u'VSE Ausbildung.odt')
    yield noteType((u"VSE Cardijn"),'appy',u'VSE Cardijn.odt')
    yield noteType((u"VSE Work & Job"),'appy',u'VSE Work & Job.odt')
    yield noteType((u"VSE Vollzeitstudium"),'appy',u'VSE Vollzeitstudium.odt')
    yield noteType((u"VSE Arbeitssuche"),'appy',u'VSE Arbeitssuche.odt')
    yield noteType((u"VSE Sprachkurs"),'appy',u'VSE Sprachkurs.odt')
    yield noteType((u"Vertrag 60-7"),'appy',u'Vertrag 60-7.odt')
    yield noteType((u"Übergabeblatt"),'appy',u'Übergabeblatt.odt')
    yield noteType((u"Neuantrag"),'appy',u'Neuantrag.odt')
    yield noteType((u"Antragsformular"),'appy',u'Antragsformular.odt')
    yield noteType((u"Recht auf Anhörung"),'appy',u'Recht auf Anhörung.odt')
    yield noteType((u"Erstgespräch"),'appy',u'Erstgespräch.odt')
    yield noteType((u"Abschlussbericht"),'appy',u'Abschlussbericht.odt')
    yield noteType((u"Notiz"),'appy','notes.Note.odt')
    yield noteType((u"Default"),'pisa','notes.Note.pisa.html')
    yield noteType((u"Externes Dokument"))
    
    excltype = Instantiator('dsbe.ExclusionType','name').build
    yield excltype(u"Termin nicht eingehalten")
    yield excltype(u"ONEM-Auflagen nicht erfüllt")
    
  
def load_tim_data(dbpath):
  
    from django.contrib.auth import models as auth
    def load(row):
        #~ auth.User.objects.create_user(row['USERID'],row['EMAIL'] or '','')
        d = name2kw(row['NAME'])
        now = datetime.datetime.now()
        if row['EMAIL']:
            user = auth.User(
                username=convert_username(row['USERID']), 
                email=row['EMAIL'],
                first_name=d['first_name'],
                last_name=d['last_name'],
                is_staff=False,is_active=True, is_superuser=False, 
                last_login=now,date_joined=now)
            user.set_password('temp')
            return user
    load_dbf(dbpath,'USR',load)
    
    def load(row):
        kw = dict(
          id=row['IDPRF'],
          name=row['LIBELL'] or '',
          lst104=row['LST104'] or False,
          )
        return Activity(**kw)
    load_dbf(dbpath,'PRF',load)

    # Countries already exist after initial_data, but their short_code is 
    # needed as lookup field for Cities.
    def load(row):
        if not row['ISOCODE']: 
            return
        try:
            country = Country.objects.get(isocode__exact=row['ISOCODE'])
        except Country.DoesNotExist,e:
            country = Country(isocode=row['ISOCODE'])
            country.name = row['NAME']
        if row['IDNAT']:
            country.short_code = row['IDNAT']
        return country
        #~ kw = dict(short_code=row['IDNAT'],name=row['NAME'],isocode=row['ISOCODE'])
        #~ return Country(**kw)
    load_dbf(dbpath,'NAT',load)
        
    def load(row):
        try:
            country = Country.objects.get(short_code__exact=row['PAYS'])
        except Country.DoesNotExist,e:
            return 
        kw = dict(
          zip_code=row['CP'] or '',
          name=row['NOM'] or '',
          country=country,
          )
        return City(**kw)
    load_dbf(dbpath,'PLZ',load)
    
    def load(row):
        if row['TYPE'] == 'MUT':
            pk = ADR_id(row['IDMUT'])
            if pk:
                d = dict(id=pk)
                d.update(street2kw(join_words(row['RUE'],row['RUENUM'],row['RUEBTE'])))
                d.update(name=row['NAME'])
                store(d,gsm=row['GSM'])
                country2kw(row,d)
                return Company(**d)
    load_dbf(dbpath,'ADR',load)
    
    
    
    def load(row):
        #~ if row['IDPRT'] != 'S':
            #~ return
        kw = {}
        kw.update(street2kw(join_words(row['RUE'],row['RUENUM'],row['RUEBTE'])))
        #~ store(kw,tim_nr=row['IDPAR'])
        store(kw,id=int(row['IDPAR']))
        
        if is_company(row):
            cl = Company
            store(kw,
              vat_id=row['NOTVA'],
              prefix=row['ALLO'],
              name=row['FIRME'],
            )
        else:
            cl = Person
            if row['IDPRT'] == 'S':
                kw.update(is_cpas=True)
            elif row['IDPRT'] == 'A':
                kw.update(is_senior=True)
            elif row['IDPRT'] == 'I':
                kw.update(is_active=False)
            kw.update(**name2kw(row['FIRME']))
            store(kw,
              national_id=row['NB2'],
              gesdos_id=row['NB1'],
              bank_account1=row['COMPTE1'],
              bank_account2=row['COMPTE2'],
              title=row['ALLO'],
            )
            if row['IDUSR']:
                try:
                    kw.update(user=auth.User.objects.get(username=row['IDUSR']))
                except auth.User.DoesNotExist,e:
                    kw.update(user=auth.User(username=row['IDUSR']))
        activity = row['PROF']
        if activity:
            try:
                activity = Activity.objects.get(pk=activity)
            except Activity.DoesNotExist:
                activity = Activity(id=activity,name=activity)
        language = isolang(row['LANGUE'])
        #~ if language:
            #~ language = Language.objects.get(pk=language)
        store(kw,
            language=language,
            activity=activity,
            remarks=row['MEMO'],
        )
        
        country2kw(row,kw)
        
        return cl(**kw)
    load_dbf(dbpath,'PAR',load)
    
    def load(row):
        #~ if row['IDPRT'] != 'S':
            #~ return
        try:
            person = Person.objects.get(pk=int(row['IDPAR']))
        except Person.DoesNotExist,e:
            return 
        pxs2person(row,person)

        return person
    load_dbf(dbpath,'PXS',load)

class Command(BaseCommand):
    args = '<path_to_tim_data_dir>'
    help = 'Performs a database reset and initial import of your TIM data'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please specify the path to your TIM data directory')
            
            
        dbname = settings.DATABASES['default']['NAME']
        if not confirm("Gonna reset your database (%s).\nAre you sure (y/n) ?" % dbname):
            raise CommandError("User abort.")
            
        call_command('reset','contacts','dsbe','countries','auth','notes','countries',interactive=False)
        
        call_command('syncdb',interactive=False)
            
        #~ NoteType = resolve_model('notes.NoteType')
        #~ n = NoteType.objects.all().count()
        #~ assert n == 21, 'NoteType.objects.all().count() == %d (expected 21)' % n

        
        #~ lino_site.initdb()
        #~ for o in tim_fixture_objects():
            #~ o.save()
        #~ lino.log.info('lino_site.fill() done. Starting load_tim_data()...')
        load_tim_data(args[0])
