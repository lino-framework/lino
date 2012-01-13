# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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

"""

import logging
logger = logging.getLogger(__name__)

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
#~ from lino.utils import crl2hex, hex2crl


from lino.modlib.contacts.utils import name2kw, street2kw, join_words
from lino.modlib.contacts.models import GENDER_MALE, GENDER_FEMALE
from lino.utils.instantiator import Instantiator

from lino.tools import resolve_model, obj2str
import lino

from lino.utils import confirm, iif
from lino.core.coretools import app_labels
from lino.apps.crl.models import CRL

Country = resolve_model('countries.Country')
City = resolve_model('countries.City')
Person = resolve_model(settings.LINO.person_model)
Company = resolve_model(settings.LINO.company_model)

def parsedate(T):
    if not T: return
    T = T.replace('.','')
    try:
        if len(T) == 4:
            return (datetime.date(int(T),6,30),True)
        elif len(T) == 6:
            return (datetime.date(int(T[:4]),int(T[4:6]),15),True)
        elif len(T) == 8:
            return (datetime.date(int(T[:4]),int(T[4:6]),int(T[6:])),False)
    except ValueError:
        pass
    dblogger.warning("Ignored invalid date value %r" % T)


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
    
    store(kw,
      phone=row['TEL'],
      fax=row['FAX'],
      email=row['EMAIL'],
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
            #~ logger.warning("%s-%s : %s",row['PAYS'],row['CP'],e)
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
    
def load_dbf(tableName,load):
    fn = os.path.join(settings.LINO.legacy_data_path,'%s.DBF' % tableName)
    f = dbfreader.DBFFile(fn,codepage="cp850")
    logger.info("Loading %d records from %s...",len(f),fn)
    f.open()
    for dbfrow in f:
        i = load(dbfrow)
        if i is not None:
            i = settings.TIM2LINO_LOCAL(tableName,i)
            if i is not None:
                try_full_clean(i)
                yield i
                    
                #~ try:
                    #~ i.save()
                #~ except Exception,e:
                    #~ dblogger.warning("Failed to save %s from %s : %s",obj2str(i),dbfrow,e)
                    #~ dblogger.exception(e)
    f.close()


def load_O_(row):
    kw = {}
    o = row['O']
    if o:
        if len(o) == 2:
            try:
                country = Country.objects.get(pk=o)
                if country.name.upper() != row['A'].upper():
                    logger.warning('Country %s : %r != %r',o,country.name,row['A'])
            except Country.DoesNotExist:
                return Country(isocode=o,name=row['A']+' <<<<')
        elif len(o) == 4:
            try:
                be = Country.objects.get(pk='BE')
                city = City.objects.get(country=be,zip_code=o)
                if city.name.upper() != row['A'].upper():
                    logger.warning('City BE-%s : %r != %r',o,city.name,row['A'])
            except City.MultipleObjectsReturned:
                logger.warning("O %s (%s) : MultipleObjectsReturned",o,row['A'])
            except City.DoesNotExist:
                return City(country=be,zip_code=o,name=row['A']+' <<<<')
        else:
            logger.warning("O %s (%s) : unknown format",o,row['A'])
                
            
def load_P_(row):
    kw = {}
    #~ kw.update(street2kw(join_words(row['RUE'],row['RUENUM'],row['RUEBTE'])))
    store(kw,last_name=row['AN'])
    store(kw,first_name=row['AP'])
    store(kw,crl=CRL(row['P'].encode('cp437')))
    #~ store(kw,crl=crl2hex(row['P']))
    OU = row['OU']
    if OU:
        kw.update(street2kw(OU))
    title = row['PQ']
    if title:
        if title == 'Mme':
            kw.update(language='fr',gender=GENDER_FEMALE)
        elif title == 'Mlle':
            kw.update(language='fr',gender=GENDER_FEMALE)
        elif title == 'M.':
            kw.update(language='fr',gender=GENDER_MALE)
        elif title == 'dHr':
            kw.update(language='nl',gender=GENDER_MALE)
        elif title == 'Mvw':
            kw.update(language='nl',gender=GENDER_FEMALE)
        elif title == 'Mr':
            kw.update(language='en',gender=GENDER_MALE)
        elif title == 'Mrs':
            kw.update(language='en',gender=GENDER_FEMALE)
        elif title == 'Hrrn':
            kw.update(language='de',gender=GENDER_MALE)
        elif title == 'Fr':
            kw.update(language='de',gender=GENDER_FEMALE)
        elif title == 'Fr.':
            kw.update(language='fr',gender=GENDER_MALE,title=u"Frère")
        elif title == 'Frl':
            kw.update(language='de',gender=GENDER_FEMALE)
        elif title == 'Bx':
            kw.update(gender=GENDER_MALE,title="Bx")
        elif title == 'Bse':
            kw.update(gender=GENDER_FEMALE,title="Bse")
        elif title == 'St':
            kw.update(gender=GENDER_MALE,title="St")
        elif title == 'Ste':
            kw.update(gender=GENDER_FEMALE,title="Ste")
        else:
            dblogger.warning("Ignored PQ value %r" % title)
      
    a = parsedate(row['T'])
    if a:
        kw.update(birth_date=a[0],birth_date_circa=a[1])
    a = parsedate(row['T'])
    if a:
        kw.update(died_date=a[0])
        if a[1]: logger.warning("Ignored 'circa' flag for died_date")
    return Person(**kw)


  
def objects():
    for i in load_dbf('P_',load_P_): yield i
    for i in load_dbf('O_',load_O_): yield i
    

