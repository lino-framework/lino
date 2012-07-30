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
#~ from lino.modlib.users.models import UserProfiles

from lino.core.modeltools import resolve_model, obj2str
from lino.core.modeltools import is_valid_email
import lino

from lino.utils import confirm, iif
from lino.core.modeltools import app_labels

Activity = resolve_model('pcsw.Activity')
Country = resolve_model('countries.Country')
City = resolve_model('countries.City')
Person = resolve_model(settings.LINO.person_model)
Company = resolve_model(settings.LINO.company_model)


users = dd.resolve_app('users')

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
      
def par_class(data):
    # wer eine nationalregisternummer hat ist eine Person, selbst wenn er auch eine MWst-Nummer hat.
    prt = data.idprt
    if prt == 'O':
        return Company
    elif prt == 'P':
        return Person
    
def store_date(row,obj,rowattr,objattr):
    v = row[rowattr]
    if v:
        if isinstance(v,basestring):
            v = dateparser.parse(v)
        setattr(obj,objattr,v)
      
      
     
def country2kw(row,kw):
    # for both PAR and ADR
    
    kw.update(created = row['datcrea'])
    country = row['pays']
    if country:
        try:
            country = Country.objects.get(short_code__exact=country)
        except Country.DoesNotExist:
            country = Country(isocode=country,name=country,short_code=country)
            country.save()
        kw.update(country=country)
    
    email = row['email']
    if email and is_valid_email(email):
        kw.update(email=email)
    store(kw,
      phone=row['tel'],
      fax=row['fax'],
      street=row['rue'],
      street_no=row['ruenum'],
      street_box=row['ruebte'],
      )
      
    #~ kw.update(street2kw(join_words(row['RUE'],row['RUENUM'],row['RUEBTE'])))
    
    zip_code = row['cp']
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
            dblogger.warning("%s-%s : %s",row['pays'],row['cp'],e)
      
        
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
    #~ fn = os.path.join(dbpath,'%s.DBF' % tableName)
    fn = os.path.join(dbpath,'%s.FOX' % tableName)
    if True:
        import dbf # http://pypi.python.org/pypi/dbf/
        table = dbf.Table(fn)
        #~ table.use_deleted = False
        table.open()
        #~ print table.structure()
        dblogger.info("Loading %d records from %s...",len(table),fn)
        for record in table:
            if not dbf.is_deleted(record):
                i = load(record)
                if i is not None:
                    yield settings.TIM2LINO_LOCAL(tableName,i)
        table.close()
    else:
        f = dbfreader.DBFFile(fn,codepage="cp850")
        dblogger.info("Loading %d records from %s...",len(f),fn)
        f.open()
        for dbfrow in f:
            i = load(dbfrow)
            if i is not None:
                yield settings.TIM2LINO_LOCAL(tableName,i)
        f.close()

    
  
def load_tim_data(dbpath):
  
    from lino.modlib.users import models as users
    
    # Countries already exist after initial_data, but their short_code is 
    # needed as lookup field for Cities.
    def load(row):
        if not row['isocode']: 
            return
        try:
            country = Country.objects.get(isocode=row['isocode'])
        except Country.DoesNotExist,e:
            country = Country(isocode=row['isocode'])
            country.name = row['name']
        if row['idnat']:
            country.short_code = row['idnat']
        return country
    yield load_dbf(dbpath,'NAT',load)
        
    def load(row):
        try:
            country = Country.objects.get(short_code=row['pays'])
        except Country.DoesNotExist,e:
            return 
        kw = dict(
          zip_code=row['cp'] or '',
          name=row['nom'] or row['cp'],
          country=country,
          )
        return City(**kw)
    yield load_dbf(dbpath,'PLZ',load)
    
    
    def load(row):
        kw = {}
        #~ kw.update(street2kw(join_words(row['RUE'],row['RUENUM'],row['RUEBTE'])))
        def par_pk(pk):
            if pk.startswith('T'):
                return 2321 + int(row.idpar[1:]) - 256 + 1
            else:
                return int(pk)
            
        store(kw,id=par_pk(row.idpar))
        
        cl = par_class(row)
        if cl is Company:
            cl = Company
            store(kw,
              vat_id=row['notva'],
              national_id_et=row['regkood'],
              prefix=row['allo'],
              name=row['firme'],
            )
        elif cl is Person:
            #~ cl = Person
            kw.update(**name2kw(row['firme']))
            store(kw,
              gender=convert_sex(row['sex']),
              first_name=row['vorname'],
              last_name=row['firme'],
              national_id_et=row['regkood'],
              #~ birth_date=row['gebdat'],
              bank_account1=row['compte1'],
              title=row['allo'],
            )
        else:
            return
        language = isolang(row['langue'])
        store(kw,
            language=language,
            remarks=row['memo'],
        )
        
        country2kw(row,kw)
        #~ print cl,kw
        return cl(**kw)
    yield load_dbf(dbpath,'PAR',load)
    

def objects():
    yield users.User(username='root',profile='900')
    for obj in load_tim_data(settings.LINO.legacy_data_path):
        yield obj