# -*- coding: UTF-8 -*-
## Copyright 2010 Luc Saffre
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

"""
Starts a daemon that 
watches the specified directory for a file :xfile:`changelog.json` 
to appear.

See also 
:doc:`/blog/2010/1210`
:doc:`/blog/2010/1211`
:doc:`/blog/2010/1214`

"""

import os
import sys
import codecs
import time
import datetime

import logging
logger = logging.getLogger(__name__)

from django.core.management.base import BaseCommand, CommandError

from lino.utils.daemoncommand import DaemonCommand

from django.conf import settings


from django.db.utils import DatabaseError
# OperationalError
from django.utils import simplejson
from django.contrib.auth import models as auth
from lino.tools import resolve_model
from lino.modlib.contacts.utils import name2kw, street2kw, join_words

from lino.utils import confirm
from lino.utils import dblogger
from lino.tools import obj2str

from lino.modlib.dsbe.management.commands.initdb_tim import convert_sex, \
    ADR_id, country2kw, pxs2person, is_company

Country = resolve_model('countries.Country')
City = resolve_model('countries.City')
Person = resolve_model('contacts.Person')
Company = resolve_model('contacts.Company')
    
def json2py(dct):
    if '__date__' in dct:
        d = dct['__date__']
        if d['year'] == 0 or d['month'] == 0 or d['day'] == 0:
            return None
        try:
            return datetime.date(d['year'], d['month'],d['day'])
        except ValueError,e:
            raise ValueError("%s : %s", dct,e)
    return dct
    

#~ def data2kw(data,kw,**d):
    #~ for k,n in d.items():
        #~ if data.has_key(n):
            #~ kw[k] = data[n]


CONTACT_FIELDS = '''id name street street_no street_box addr1 
country city zip_code region language email url phone gsm remarks'''.split()


class Controller:
    def applydata(self,obj,data,**d):
        for k,v in d.items():
            if data.has_key(v):
                setattr(obj,k,data[v])
        obj = settings.TIM2LINO_LOCAL(self.__class__.__name__,obj)
        obj.full_clean()
                
    def POST(self,**kw):
        obj = self.model()
        self.applydata(obj,kw['data'])
        obj.save()
        dblogger.debug("%s:%s : POST %s",kw['alias'],kw['id'],kw['data'])
        
    def DELETE(self,**kw):
        obj = self.get_object(kw)
        if obj is None:
            dblogger.debug("%s:%s : DELETE failed (does not exist)",kw['alias'],kw['id'])
            return
        obj.delete()
        dblogger.debug("%s:%s : DELETE ok",kw['alias'],kw['id'])
                    
    def PUT(self,**kw):
        obj = self.get_object(kw)
        if obj is None:
            dblogger.debug("%s:%s : PUT becomes POST",kw['alias'],kw['id'])
            kw['method'] = 'POST'
            return self.POST(**kw)
        if self.PUT_special(obj,**kw):
            return 
        self.applydata(obj,kw['data'])
        obj.save()
        dblogger.debug("%s:%s : PUT %s",kw['alias'],kw['id'],kw['data'])
        
    def PUT_special(self,obj,**kw):
        pass
        
def ADR_applydata(obj,data,**d):        
    d.update(
        street='RUE',
        street_box='RUEBTE',
        phone='TEL',
    )
    if data.has_key('RUENUM'):
        obj.street_no = data['RUENUM'].strip()
    kw = {}
    country2kw(data,kw)
    for k,v in kw.items():
        setattr(obj,k,v)
        
    #~ if d.has_key('PAYS'):
        #~ try:
            #~ obj.country = Country.objects.get(short_code__exact=data['PAYS'])
        #~ except Country.DoesNotExist,e:
            #~ pass
    #~ if d.has_key('CP'):
        #~ try:
            #~ obj.city = City.objects.get(short_code__exact=data['PAYS'])
        #~ except Country.DoesNotExist,e:
            #~ pass
                
class PAR(Controller):
  
    def applydata(self,obj,data,**d):
        d.update(
            id='IDPAR',
            remarks='MEMO',
            national_id='NB2',
            bank_account1='COMPTE1',
            bank_account2='COMPTE2',
        )
        ADR_applydata(obj,data,**d)
        #~ kw.update(street2kw(join_words(data['RUE'],
        if obj.__class__ is Person:
            d.update(title='ALLO')
            d.update(gesdos_id='NB1')
            if data.has_key('IDUSR'):  
                username = settings.TIM2LINO_USERNAME(data['IDUSR'])
                if username is not None:
                    try:
                        obj.user = auth.User.objects.get(username=username)
                    except auth.User.DoesNotExist,e:
                        dblogger.warning(u"%s : PAR->IdUsr %r (converted to %r) doesn't exist!",obj2str(obj),data['IDUSR'],username)
            if data.has_key('FIRME'):  
                for k,v in name2kw(data['FIRME']).items():
                    setattr(obj,k,v)
        if obj.__class__ is Company:
            d.update(prefix='ALLO')
            d.update(vat_id='NOTVA')
        Controller.applydata(self,obj,data,**d)
        
    def swapclass(self,obj,new_class,data):
        kw = {}
        for n in CONTACT_FIELDS:
            kw[n] = getattr(obj,n)
            v = data.get(n,None)
            if v is not None:
                kw[n] = v
        newobj = new_class(**kw)
        self.applydata(newobj,data)
        newobj.save()
        obj.delete()
        
    def get_object(self,kw):
        id = kw['id']
        try:
            return Person.objects.get(pk=id)
        except Person.DoesNotExist:
            try:
                return Company.objects.get(pk=id)
            except Company.DoesNotExist:
                pass
        
    def PUT_special(self,obj,**kw):
        #~ vat_id = kw['data'].get('NOTVA',None)
        #~ if vat_id:
        if is_company(kw['data']):
            if obj.__class__ is Person:
                dblogger.debug("%s:%s : Person becomes Company",kw['alias'],kw['id'])
                self.swapclass(obj,Company,kw['data'])
                return True
        else:
            if obj.__class__ is Company:
                dblogger.debug("%s:%s : Company becomes Person",kw['alias'],kw['id'])
                self.swapclass(obj,Person,kw['data'])
                return True
            
    def POST(self,**kw):
        #~ vat_id = kw['data'].get('NOTVA',None)
        #~ if vat_id:
        if is_company(kw['data']):
            obj = Company()
        else:
            obj = Person()
        self.applydata(obj,kw['data'])
        obj.save()
        dblogger.debug("%s:%s : POST %s",kw['alias'],kw['id'],kw['data'])
            

class PXS(PAR):
    def applydata(self,obj,data,**d):
        d.update(
            card_number='CARDNUMBER',
            birth_place='BIRTHPLACE',
            birth_date='GEBDAT',
        )
        Controller.applydata(self,obj,data,**d)
        
        pxs2person(data,obj)
        
        
class PLZ(PAR):
  
    model = City
    
    def get_object(self,kw):
        id = kw['id']
        if len(id) != 2:
            raise Exception("%r : invalid id for PLZ" % id)
        try:
            return self.model.objects.get(
              country__short_code__exact=id[0],
              zip_code__exact=id[1],
              )
        except self.model.DoesNotExist:
            pass
            
    def applydata(self,obj,data,**d):
        d.update(
            name='NOM',
            zip_code='CP',
        )
        try:
            obj.country = Country.objects.get(short_code__exact=data['PAYS'])
        except Country.DoesNotExist:
            pass  
        Controller.applydata(self,obj,data,**d)

class NAT(Controller):
  
    model = Country
    
    def get_object(self,kw):
        id = kw['id']
        try:
            return Country.objects.get(short_code__exact=id)
        except Country.DoesNotExist:
            pass
            
    def applydata(self,obj,data,**d):
        d.update(
            short_code='IDNAT',
            name='NAME',
            isocode='ISOCODE',
        )
        Controller.applydata(self,obj,data,**d)


class ADR(Controller):
  
    model = Company
    
    def get_object(self,kw):
        idmut = kw['data']['IDMUT']
        if idmut:
            try:
                return Company.objects.get(id__exact=ADR_id(idmut))
            except Country.DoesNotExist:
                pass
            
    def applydata(self,obj,data,**d):
        d.update(
            name='NAME',
        )
        ADR_applydata(obj,data,**d)
        Controller.applydata(self,obj,data,**d)


controllers = dict(
  NAT=NAT(),
  PLZ=PLZ(),
  PAR=PAR(),
  PXS=PXS(),
  ADR=ADR(),
  )

def process_line(i,ln):
    d = simplejson.loads(ln,object_hook=json2py)
    kw = {}
    for k,v in d.items():
        kw[str(k)] = v
    ctrl = controllers.get(kw['alias'],None)
    if ctrl is None:
        raise Exception("%(alias)s : no such controller." % kw)
        #~ logger.debug("Ignoring change %s for %(alias)s:%(id)s",kw['time'],kw['alias'],kw['id'])
        #~ return
    m = getattr(ctrl,kw['method'])
    m(**kw)
    #~ n = 0
    #~ while True:
        #~ try:
            #~ m(**kw)
            #~ return
        #~ except Exception,e:
            #~ n += 1
            #~ if n > 9:
                #~ raise
            #~ logger.warning("Got %r (will retry %d)",e,n)
            #~ time.sleep(1)
        
    #~ ctrl.process(**kw)
    
  
def watch(data_dir):
    infile = os.path.join(data_dir,'changelog.json')
    watching = os.path.join(data_dir,'changelog.watching.json')
    failed = os.path.join(data_dir,'changelog.failed.json')
    if not os.path.exists(watching):
        if not os.path.exists(infile):
            #~ print "Nothing to do."
            return
        try:
            os.rename(infile,watching)
        except Exception,e:
            #~ logger.debug("Could not rename %s to %s",infile,watching)
            return
    dblogger.info("Processing file %s",watching)
    fd_watching = codecs.open(watching,'r',encoding='cp850')
    fd_failed = codecs.open(failed,'a',encoding='cp850')
    #~ log = open(os.path.join(data_dir,'changelog.done.log'),'a')
    i = 0
    for ln in fd_watching:
        i += 1
        try:
            process_line(i,ln)
        except Exception,e:
            fd_failed.write("// %s %r\n%s\n\n" % (time.strftime("%Y-%m-%d %H:%M:%S"),e,ln))
            #~ fd_failed.write(ln+'\n')
            dblogger.warning("%s:%d: %r", watching,i,e)
            dblogger.exception(e)
            #~ raise
    fd_watching.close()
    fd_failed.close()
    os.remove(watching)
    dblogger.info("%d changes have been processed.",i)
    #~ log.close()
        

def main(*args,**options):
    if len(args) != 1:
        raise CommandError('Please specify the path to your TIM changelog directory')
    data_dir = args[0]
    logger.info("Started tim_watch on %s ...",data_dir)
    dblogger.info("Watching %s ...",data_dir)
    #~ last_warning = None
    while True:
        watch(data_dir)
        time.sleep(1)

class Command(DaemonCommand):
  
    args = '<path_to_tim_changelog>'
    help = 'Starts an observer service that propagates changes of your TIM data into Lino'
    
    #~ stdout = '/var/log/lino/watch_tim.log' 
    #~ stdout = os.path.join(settings.PROJECT_DIR, "watch_tim","stdout.log")
    #~ stderr = '/var/log/lino/watch_tim.errors.log' 
    #~ os.path.join(settings.PROJECT_DIR, "watch_tim","errors.log")
    #~ pidfile = os.path.join(settings.PROJECT_DIR, "watch_tim","pid")
    #~ pidfile = '/var/run/watch_tim.pid' # os.path.j    
    
    preserve_loggers = (logger,dblogger.logger)
    
    def handle_daemon(self, *args, **options):
        main(*args,**options)


    def handle(self, *args, **options):
        logger.info("handle(%r,%r)",args,options)
        dblogger.info("handle(%r,%r)",args,options)
        return DaemonCommand.handle(self,*args,**options)
