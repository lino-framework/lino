# -*- coding: UTF-8 -*-
## Copyright 2010-2011 Luc Saffre
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
#~ import signal
import atexit

#~ import logging
#~ logger = logging.getLogger(__name__)

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError


from django.conf import settings


from django.db.utils import DatabaseError
# OperationalError
from django.utils import simplejson
#~ from django.contrib.auth import models as auth
from lino.modlib.users import models as auth

import lino

from lino.tools import resolve_model
from lino.modlib.contacts.utils import name2kw, street2kw, join_words

from lino.utils import confirm
from lino.utils import dblogger
from lino.utils import mti
from lino.tools import obj2str

from lino.utils.daemoncommand import DaemonCommand

#~ from lino.apps.dsbe.models  import is_valid_niss

from lino.apps.dsbe.management.commands.initdb_tim import convert_sex, \
    ADR_id, country2kw, par2person, pxs2person, is_company

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


CONTACT_FIELDS = '''id name street street_no street_box addr2 
country city zip_code region language email url phone gsm remarks'''.split()

class PseudoRequest:
    user = "watch_tim"

REQUEST = PseudoRequest()

class Controller:
    "Deserves more documentation."
    allow_put2post = True
    def applydata(self,obj,data,**mapper):
        """
        Stores values from `data` into `obj` using mapper.
        `mapper` is a `dict` whose keys are Lino field names and whose values are TIM field names.
        e.g. something like `dict(id='IDPAR',street='STREET')`.
        Deserves more documentation.
        """
        for lino_name,tim_name in mapper.items():
            if data.has_key(tim_name):
                setattr(obj,lino_name,data[tim_name])
        settings.TIM2LINO_LOCAL(self.__class__.__name__,obj)
        
    def validate_and_save(self,obj):
        "Deserves more documentation."
        try:
            obj.full_clean()
            dblogger.log_changes(REQUEST,obj)
            obj.save()
        except ValidationError,e:
            # here we only log an obj2str() of the object 
            # full traceback will be logged in watch() after process_line()
            dblogger.warning("Validation failed for %s : %s",obj2str(obj),e)
            raise # re-raise (propagate) exception with original traceback
            #~ dblogger.exception(e)
                
    def get_object(self,kw):
        raise NotImplementedError
        
    def DELETE(self,**kw):
        obj = self.get_object(kw)
        if obj is None:
            dblogger.warning("%s:%s : DELETE failed (does not exist)",
                kw['alias'],kw['id'])
            return
        dblogger.log_deleted(REQUEST,obj)
        obj.delete()
        dblogger.debug("%s:%s (%s) : DELETE ok",kw['alias'],kw['id'],obj2str(obj))
        
    #~ def prepare_data(self,data):
        #~ return data
        
    def create_object(self,kw):
        return self.model()
                    
    def POST(self,**kw):
        #~ self.prepare_data(kw['data'])
        obj = self.get_object(kw)
        if obj is None:
            obj = self.create_object(kw)
            if obj is None:
                dblogger.warning("%s:%s (%s) : ignored POST %s",
                    kw['alias'],kw['id'],obj,kw['data'])
                return
        else:
            dblogger.info("%s:%s : POST becomes PUT",kw['alias'],kw['id'])
        self.applydata(obj,kw['data'])
        self.validate_and_save(obj)
        #~ obj.save()
        dblogger.debug("%s:%s (%s) : POST %s",kw['alias'],kw['id'],obj2str(obj),kw['data'])
        
    def PUT(self,**kw):
        obj = self.get_object(kw)
        if obj is None:
            if self.allow_put2post:
                dblogger.info("%s:%s : PUT becomes POST",kw['alias'],kw['id'])
                kw['method'] = 'POST'
                return self.POST(**kw)
            else:
                dblogger.warning("%s:%s : PUT ignored (row does not exist)",kw['alias'],kw['id'])
                return 
        if self.PUT_special(obj,**kw):
            return 
        self.applydata(obj,kw['data'])
        self.validate_and_save(obj)
        #~ obj.save()
        #~ dblogger.debug("%s:%s : PUT %s",kw['alias'],kw['id'],kw['data'])
        dblogger.debug("%s:%s (%s) : PUT %s",kw['alias'],kw['id'],obj2str(obj),kw['data'])
        
    def PUT_special(self,obj,**kw):
        pass
        
def ADR_applydata(obj,data,**kw):
    #~ kw.update(
        #~ street='RUE',
        #~ street_box='RUEBTE',
        #~ phone='TEL',
    #~ )
    #~ if data.has_key('RUENUM'):
        #~ obj.street_no = data['RUENUM'].strip()
    #~ kw = {}
    country2kw(data,kw)
    for k,v in kw.items():
        setattr(obj,k,v)
                
class PAR(Controller):
    "Deserves more documentation."
  
    #~ def prepare_data(self,data):
        #~ if data['NB2']:
            #~ if not is_valid_niss(data['NB2']):
                #~ dblogger.warning("Ignored invalid NISS %s" % data['NB2'])
                #~ data['NB2'] = ''
        #~ return data
                
    def applydata(self,obj,data,**mapper):
        mapper.update(
            id='IDPAR', 
            remarks='MEMO',
            national_id='NB2',
            bank_account1='COMPTE1',
            bank_account2='COMPTE2',
        )
        ADR_applydata(obj,data) # ,**mapper)
        #~ kw.update(street2kw(join_words(data['RUE'],
        if obj.__class__ is Person:
            par2person(data,obj)
            mapper.update(title='ALLO')
            mapper.update(gesdos_id='NB1')
            if data.has_key('IDUSR'):
                username = settings.TIM2LINO_USERNAME(data['IDUSR'])
                if username:
                    try:
                        obj.coach1 = auth.User.objects.get(username=username)
                    except auth.User.DoesNotExist,e:
                        dblogger.warning(
                          u"%s : PAR->IdUsr %r (converted to %r) doesn't exist!",
                          obj2str(obj),data['IDUSR'],username)
                else:
                    obj.coach1 = None
                    #~ obj.user = None
            if data.has_key('FIRME'):
                for k,v in name2kw(data['FIRME']).items():
                    setattr(obj,k,v)
        if obj.__class__ is Company:
            mapper.update(prefix='ALLO')
            mapper.update(vat_id='NOTVA')
            mapper.update(name='FIRME')
        Controller.applydata(self,obj,data,**mapper)
        
    def swapclass(self,obj,new_class,data):
        kw = {}
        for n in CONTACT_FIELDS:
            kw[n] = getattr(obj,n)
            v = data.get(n,None)
            if v is not None:
                kw[n] = v
        old_class = obj.__class__
        obj = obj.contact_ptr
        mti.delete_child(obj,old_class)
        newobj = mti.insert_child(obj,new_class)
        #~ obj.delete()
        #~ newobj = new_class(**kw)
        self.applydata(newobj,data)
        self.validate_and_save(newobj)
        #~ newobj.save()
        
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
                dblogger.info("%s:%s (%s) : Person becomes Company",kw['alias'],kw['id'],obj2str(obj))
                self.swapclass(obj,Company,kw['data'])
                return True
        else:
            if obj.__class__ is Company:
                dblogger.info("%s:%s (%s) : Company becomes Person",kw['alias'],kw['id'],obj2str(obj))
                self.swapclass(obj,Person,kw['data'])
                return True
            
    def create_object(self,kw):
        if is_company(kw['data']):
            return Company()
        else:
            return Person()
      
    #~ def POST(self,**kw):
        #~ self.applydata(obj,kw['data'])
        #~ self.validate_and_save(obj)
        #~ dblogger.debug("%s:%s (%s): POST %s",kw['alias'],kw['id'],obj,kw['data'])
            

class PXS(Controller):
    "Controller for importing PXS changes to Person."
  
    allow_put2post = False
    """This is False because the following case cannot be resolved: 
    a Person that exists in TIM but not in Lino gets her PXS modified in TIM. 
    TIM issues a PUT on PXS. Lino cannot convert this into a POST and create 
    the person because e.g. name ist not known.
    
    TIM schreibt beim Erstellen eines neuen Partners logischerweise 
    sowohl für PAR als auch für PXS ein POST. Weil die beiden in Lino 
    aber eine einzige Tabelle sind, bekamen wir dann beim POST des PXS 
    eine Fehlermeldung "Partner with this id already exists".
        
    """
    
    def create_object(self,kw):
        raise Exception("Tried to create a Person from PXS")
        
    def PUT_special(self,obj,**kw):
        pass
        
    def get_object(self,kw):
        id = kw['id']
        try:
            return Person.objects.get(pk=id)
        except Person.DoesNotExist:
            pass
            
    def applydata(self,obj,data,**d):
        d.update(
            card_number='CARDNUMBER',
            birth_place='BIRTHPLACE',
            birth_date='GEBDAT',
        )
        Controller.applydata(self,obj,data,**d)
        pxs2person(data,obj)
        
    #~ def POST(self,**kw):
        #~ """Deserves more documentation."""
        # Don't use the POST defined in PAR!
        #~ return Controller.POST(self,**kw)
        #~ self.PUT(**kw)
        
        
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
    u"""
    Aus ADR werden nur die Krankenkassen (d.h. ADR->IdMut nicht leer)
    nach Lino übernommen, 
    wobei `Company.id = 199000 + int(ADR->IdMut)`.
    """
    model = Company
    
    def create_object(self,kw):
        "Returns None if ADR->IdMut is empty or invalid."
        idmut = kw['data']['IDMUT']
        if idmut:
            pk = ADR_id(idmut)
            if pk:
                return Company(id=pk)
      
    def get_object(self,kw):
        idmut = kw['data']['IDMUT']
        if idmut:
            pk = ADR_id(idmut)
            if pk:
                try:
                    return Company.objects.get(id__exact=pk)
                except Company.DoesNotExist:
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
    dblogger.debug("process_line(%r,%r)",i,ln)
    d = simplejson.loads(ln,object_hook=json2py)
    kw = {}
    for k,v in d.items():
        kw[str(k)] = v
    ctrl = controllers.get(kw['alias'],None)
    if ctrl is None:
        raise Exception("%(alias)s : no such controller." % kw)
        #~ logger.debug("Ignoring change %s for %(alias)s:%(id)s",kw['time'],kw['alias'],kw['id'])
        #~ return
    #~ kw['data'] = ctrl.prepare_data(kw['data'])
    m = getattr(ctrl,kw['method'])
    m(**kw)
    
  
def watch(data_dir):
    "Deserves more documentation."
    infile = os.path.join(data_dir,'changelog.json')
    if not os.path.exists(infile):
        #~ print "Nothing to do."
        return
        
    watching = os.path.join(data_dir,'changelog.watching.json')
    if not os.path.exists(watching):
        try:
            os.rename(infile,watching)
        except Exception,e:
            dblogger.debug("Could not rename %s to %s",infile,watching)
            return
    dblogger.info("Processing file %s",watching)
    fd_watching = codecs.open(watching,'r',encoding='cp850')
    
    failed = os.path.join(data_dir,'changelog.failed.json')
    fd_failed = codecs.open(failed,'a',encoding='cp850')
    #~ log = open(os.path.join(data_dir,'changelog.done.log'),'a')
    i = 0
    for ln in fd_watching.readlines():
        i += 1
        try:
            process_line(i,ln)
        except Exception,e:
            fd_failed.write("// %s %r\n%s\n\n" % (
                time.strftime("%Y-%m-%d %H:%M:%S"),e,ln))
            #~ fd_failed.write(ln+'\n')
            #~ dblogger.warning("%s:%d: %r\nin changelog line %s", watching,i,e,ln)
            dblogger.warning(
                "Exception '%s' while processing changelog line:\n%s", 
                e,ln)
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
    msg = "Started watch_tim %s on %s ..."
    #~ logger.info(msg,data_dir)
    dblogger.info(msg,lino.__version__,data_dir)
        
    def goodbye():
        msg = "Stopped watch_tim %s on %s ..."
        #~ logger.info(msg,data_dir)
        dblogger.info(msg,lino.__version__,data_dir)
    #~ signal.signal(signal.SIGTERM,on_SIGTERM)
    atexit.register(goodbye)
    
    #~ last_warning = None
    while True:
        try:
            watch(data_dir)
        except Exception,e:
            dblogger.exception(e)
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
    
    #~ preserve_loggers = (logger,dblogger.logger)
    preserve_loggers = [dblogger.logger]
    
    def handle_daemon(self, *args, **options):
        main(*args,**options)


    #~ def handle(self, *args, **options):
        #~ logger.info("handle(%r,%r)",args,options)
        #~ dblogger.info("handle(%r,%r)",args,options)
        #~ return DaemonCommand.handle(self,*args,**options)
