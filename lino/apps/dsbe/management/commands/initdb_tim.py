# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
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
## along with Lino ; if not, see <http://www.gnu.org/licenses/>.

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

#~ from lino import lino_site
from lino.utils import dbfreader
from lino.utils import dblogger
#~ from lino import diag

from lino.modlib.contacts.utils import name2kw, street2kw
from lino.utils import join_words
#~ from lino.modlib.contacts.models import name2kw, street2kw, join_words
from lino.utils.instantiator import Instantiator

from lino.tools import resolve_model, obj2str
from lino.tools import is_valid_email
import lino

from lino.utils import confirm, iif
from lino.core.coretools import app_labels

Activity = resolve_model('dsbe.Activity')
Country = resolve_model('countries.Country')
City = resolve_model('countries.City')
Person = resolve_model(settings.LINO.person_model)
Company = resolve_model(settings.LINO.company_model)


def store(kw,**d):
    for k,v in d.items():
        if v is not None:
        # see :doc:`/blog/2011/0711`
        #~ if v:
            kw[k] = v

#~ def convert_username(name):
    #~ return name.lower()
  
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
    
def store_date(row,obj,rowattr,objattr):
    v = row[rowattr]
    if v:
        if isinstance(v,basestring):
            v = dateparser.parse(v)
        setattr(obj,objattr,v)
      
      
def ADR_id(cIdAdr):
    assert len(cIdAdr) == 3
    #~ assert [cIdAdr:-3] == '000'
    try:
        return 199000+int(cIdAdr)
    except ValueError,e:
        return None

     
def country2kw(row,kw):
    # for both PAR and ADR
    
    if row.has_key('PROF'):
        activity = row['PROF']
        if activity:
            try:
                activity = int(activity)
            except ValueError:
                dblogger.debug("Ignored invalid value PROF = %r",activity)
            else:
                if activity:
                    try:
                        activity = Activity.objects.get(pk=activity)
                    except Activity.DoesNotExist:
                        activity = Activity(id=activity,name=unicode(activity))
                        activity.save(force_insert=True)
                    kw.update(activity=activity)
        
    country = row['PAYS']
    if country:
        try:
            country = Country.objects.get(short_code__exact=country)
        except Country.DoesNotExist:
            country = Country(isocode=country,name=country,short_code=country)
            country.save()
        kw.update(country=country)
    
    email = row['EMAIL']
    if email and is_valid_email(email):
        kw.update(email=email)
    store(kw,
      phone=row['TEL'],
      fax=row['FAX'],
      )
      
    kw.update(street2kw(join_words(row['RUE'],row['RUENUM'],row['RUEBTE'])))
    
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
            #~ dblogger.warning("%s-%s : %s",row['PAYS'],row['CP'],e)
        except City.MultipleObjectsReturned,e:
            dblogger.warning("%s-%s : %s",row['PAYS'],row['CP'],e)
      
def par2person(row,person):
    person.is_active = iif(row['IDPRT']=='I',False,True)
    if row['IDPRT'] == 'S':
        person.is_cpas = True
    elif row['IDPRT'] == 'A':
        person.is_senior = True
        
def pxs2person(row,person):
  
    kw = {}
    store(kw,
      card_number=row['CARDNUMBER'],
      card_type=row.get('CARDTYPE',''),      # 20110110
      card_issuer=row.get('CARDISSUER',''),      # 20110110
      noble_condition=row.get('NOBLEECOND',''),      # 20110110
      birth_place=row.get('BIRTHPLACE',''),
      remarks2=row.get('MEMO',''),
      gender=convert_sex(row['SEXE'])
    )
    for k,v in kw.items():
        setattr(person,k,v)
    
    par2person(row,person)    
        
    if row['IDMUT']:
        try:
            person.health_insurance = Company.objects.get(pk=ADR_id(row['IDMUT']))
        except ValueError,e:
            dblogger.warning(u"%s : invalid health_insurance %r",obj2str(person),row['IDMUT'])
        except Company.DoesNotExist,e:
            dblogger.warning(u"%s : health_insurance %s not found",obj2str(person),row['IDMUT'])
  
    if row['APOTHEKE']:
        try:
            person.pharmacy = Company.objects.get(pk=int(row['APOTHEKE']))
        except ValueError,e:
            dblogger.warning(u"%s : invalid pharmacy %r",obj2str(person),row['APOTHEKE'])
        except Company.DoesNotExist,e:
            dblogger.warning(u"%s : pharmacy %s not found",obj2str(person),row['APOTHEKE'])
            
    nat = row['NATIONALIT']
    if nat:
        try:
            country = Country.objects.get(short_code__exact=nat)
        except Country.DoesNotExist:
            country = Country(isocode=nat,name=nat,short_code=nat)
            country.save()
        person.nationality=country
        
    store_date(row,person,'GEBDAT','birth_date')
    store_date(row,person,'VALID1','card_valid_from')
    store_date(row,person,'VALID2','card_valid_until')
            
        
def try_full_clean(i):
    while True:
        try:
            i.full_clean()
        except ValidationError,e:
            if not hasattr(e, 'message_dict'):
                raise
            for k in e.message_dict.keys():
                fld = i._meta.get_field(k)
                v = getattr(i,k)
                setattr(i,k,fld.default)
                dblogger.warning("%s : ignoring value %r for %s : %s",obj2str(i),v,k,e)
        return
    
def load_dbf(dbpath,tableName,load):
    fn = os.path.join(dbpath,'%s.DBF' % tableName)
    f = dbfreader.DBFFile(fn,codepage="cp850")
    dblogger.info("Loading %d records from %s...",len(f),fn)
    f.open()
    for dbfrow in f:
        i = load(dbfrow)
        if i is not None:
            i = settings.TIM2LINO_LOCAL(tableName,i)
            if i is not None:
              
                try_full_clean(i)
                    
                try:
                    i.save()
                    #~ dblogger.debug("%s has been saved",i)
                except Exception,e:
                #~ except IntegrityError,e:
                    dblogger.warning("Failed to save %s from %s : %s",obj2str(i),dbfrow,e)
                    dblogger.exception(e)
    f.close()

    
  
def load_tim_data(dbpath):
  
    #~ from django.contrib.auth import models as auth
    from lino.modlib.users import models as auth
    def load(row):
        #~ auth.User.objects.create_user(row['USERID'],row['EMAIL'] or '','')
        if not row['EMAIL']:
            return
        username = settings.TIM2LINO_USERNAME(row['USERID'])
        if username is None:
            return
        d = name2kw(row['NAME'],False)
        now = datetime.datetime.now()
        user = auth.User(
            username=username, 
            #~ username=row['USERID'].lower(), 
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
          lst104=(row['LST104'] in ('X','x')),
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
          name=row['NOM'] or row['CP'],
          country=country,
          )
        return City(**kw)
    load_dbf(dbpath,'PLZ',load)
    
    def load(row):
        if row['TYPE'] == 'MUT':
            pk = ADR_id(row['IDMUT'])
            if pk:
                d = dict(id=pk)
                d.update(name=row['NAME'])
                #~ 20101230 store(d,gsm=row['GSM'])
                country2kw(row,d)
                return Company(**d)
    load_dbf(dbpath,'ADR',load)
    
    
    
    def load(row):
        kw = {}
        #~ kw.update(street2kw(join_words(row['RUE'],row['RUENUM'],row['RUEBTE'])))
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
                username = settings.TIM2LINO_USERNAME(row['IDUSR'])
                if username is not None:
                    try:
                        kw.update(coach1=auth.User.objects.get(username=username))
                        #~ kw.update(user=auth.User.objects.get(username=username))
                    except auth.User.DoesNotExist,e:
                        dblogger.warning("PAR:%s PAR->IdUsr %r (converted to %r) doesn't exist!",row['IDPAR'],row['IDUSR'],username)
        language = isolang(row['LANGUE'])
        #~ if language:
            #~ language = Language.objects.get(pk=language)
        store(kw,
            language=language,
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
            
        options.update(interactive=False)
        
        dblogger.info("Lino initdb_tim started on database %s." % dbname)
        dblogger.info(lino.welcome_text())
            
        apps = app_labels()
        call_command('reset',*apps,**options)
        
        #~ call_command('reset',
          #~ 'contacts','dsbe','countries','auth','notes',
          #~ 'countries','links','uploads',
          #~ interactive=False)
        
        call_command('syncdb',**options)
            
        #~ NoteType = resolve_model('notes.NoteType')
        #~ n = NoteType.objects.all().count()
        #~ assert n == 21, 'NoteType.objects.all().count() == %d (expected 21)' % n

        
        #~ lino_site.initdb()
        #~ for o in tim_fixture_objects():
            #~ o.save()
        #~ logger.info('lino_site.fill() done. Starting load_tim_data()...')
        load_tim_data(args[0])
        
        dblogger.info("Lino initdb_tim done on database %s." % dbname)
