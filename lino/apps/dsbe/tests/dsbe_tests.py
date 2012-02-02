# -*- coding: utf-8 -*-
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
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This module contains "quick" tests that are run on a demo database 
without any fixture. You can run only these tests by issuing::

  python manage.py test dsbe.QuickTest

  
"""
import logging
logger = logging.getLogger(__name__)

#~ from django.utils import unittest
#~ from django.test.client import Client
from django.conf import settings

#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
#~ from lino.modlib.contacts.models import Companies


from lino.utils import i2d
from lino.utils import babel
from lino.tools import resolve_model
#Companies = resolve_model('contacts.Companies')
from lino.utils.test import TestCase

#~ Person = resolve_model('contacts.Person')
#~ Property = resolve_model('properties.Property')
#~ PersonProperty = resolve_model('properties.PersonProperty')

from lino.apps.dsbe.models import Person, PersonProperty
from lino.modlib.properties.models import Property



class QuickTest(TestCase):
    pass
    #~ def setUp(self):
        #~ settings.LINO.auto_makeui = False
        #~ super(DemoTest,self).setUp()
            
  
def test01(self):
    """
    Used on :doc:`/blog/2011/0414`.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_tests.py`.
    """
    from lino.utils.dpy import Serializer
    from lino.apps.dsbe.models import Contact, Company
    ser = Serializer()
    #~ ser.models = [CourseProvider,Company]
    ser.models = [Contact, Company]
    ser.write_preamble = False
    self.assertEqual(Contact._meta.parents,{})
    parent_link_field = Company._meta.parents.get(Contact)
    #~ print parent_link_field.name
    #~ self.assertEqual(CourseProvider._meta.parents.get(Company),{})
    #~ self.assertEqual(CourseProvider._meta.parents,{})
    fields = [f.attname for f in Company._meta.fields]
    local_fields = [f.attname for f in Company._meta.local_fields]
    #~ self.assertEqual(','.join(local_fields),'contact_ptr_id')
    self.assertEqual(','.join(local_fields),'contact_ptr_id,vat_id,type_id,is_active,activity_id,bank_account1,bank_account2,prefix,hourly_rate')
    fields = [f.attname for f in Contact._meta.fields]
    local_fields = [f.attname for f in Contact._meta.local_fields]
    self.assertEqual(fields,local_fields)
    #~ self.assertTrue(','.join([f.attname for f in local_fields]),'company_ptr_id')
      
    #~ foo = Company(name='Foo')
    #~ foo.save()
    bar = Contact(name='Bar')
    bar.save()
    
    #~ ser.serialize([foo,bar])
    ser.serialize([bar])
    #~ print ser.stream.getvalue()
    expected = """
def create_contacts_contact(id, country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks):
    return contacts_Contact(id=id,country_id=country_id,city_id=city_id,name=name,addr1=addr1,street_prefix=street_prefix,street=street,street_no=street_no,street_box=street_box,addr2=addr2,zip_code=zip_code,region=region,language=language,email=email,url=url,phone=phone,gsm=gsm,fax=fax,remarks=remarks)
def create_contacts_company(contact_ptr_id, vat_id, type_id, is_active, activity_id, bank_account1, bank_account2, prefix, hourly_rate):
    return insert_child(contacts_Contact.objects.get(pk=contact_ptr_id),contacts_Company,vat_id=vat_id,type_id=type_id,is_active=is_active,activity_id=activity_id,bank_account1=bank_account1,bank_account2=bank_account2,prefix=prefix,hourly_rate=hourly_rate)


def contacts_contact_objects():
    yield create_contacts_contact(100,None,None,u'Bar',u'',u'',u'',u'',u'',u'',u'',u'',u'de',u'',u'',u'',u'',u'',u'')


def objects():
    yield contacts_contact_objects()

settings.LINO.loading_from_dump = True

from lino.apps.dsbe.migrate import install
install(globals())
"""
    self.assertEqual(ser.stream.getvalue(),expected)
    
def test01(self):
    """
    Used on :doc:`/blog/2011/0414`.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_tests.py`.
    """
    from lino.utils.dpy import Serializer
    from lino.apps.dsbe.models import Company, CourseProvider
    ser = Serializer()
    #~ ser.models = [CourseProvider,Company]
    ser.models = [CourseProvider]
    ser.write_preamble = False
    self.assertEqual(Company._meta.parents,{})
    parent_link_field = CourseProvider._meta.parents.get(Company)
    #~ print parent_link_field.name
    #~ self.assertEqual(CourseProvider._meta.parents.get(Company),{})
    #~ self.assertEqual(CourseProvider._meta.parents,{})
    fields = [f.attname for f in CourseProvider._meta.fields]
    local_fields = [f.attname for f in CourseProvider._meta.local_fields]
    self.assertEqual(','.join(local_fields),'company_ptr_id')
    fields = [f.attname for f in Company._meta.fields]
    local_fields = [f.attname for f in Company._meta.local_fields]
    self.assertEqual(fields,local_fields)
    #~ self.assertTrue(','.join([f.attname for f in local_fields]),'company_ptr_id')
      
    #~ foo = Company(name='Foo')
    #~ foo.save()
    bar = CourseProvider(name='Bar')
    bar.save()
    
    #~ ser.serialize([foo,bar])
    ser.serialize([bar])
    #~ print ser.stream.getvalue()
    self.assertEqual(ser.stream.getvalue(),"""
def create_dsbe_courseprovider(company_ptr_id):
    return insert_child(Company.objects.get(pk=company_ptr_id),CourseProvider)


def dsbe_courseprovider_objects():
    yield create_dsbe_courseprovider(1)


def objects():
    for o in dsbe_courseprovider_objects(): yield o

from lino.apps.dsbe.migrate import install
install(globals())
""")
test01.skip = True

def test01b(self):
    """
    Tests error handling when printing a contract whose type's 
    name contains non-ASCII char.
    Created :doc:`/blog/2011/0615`.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_tests.py`.
    """
    from lino.modlib.jobs.models import Contracts, Contract, ContractType, JobProvider, Job
    #~ from lino.modlib.notes.models import ContractType
    from lino.mixins.printable import PrintAction
    from lino.modlib.users.models import User
    from lino.apps.dsbe.models import Person
    root = User(username='root') # ,last_name="Superuser")
    root.save()
    jp = JobProvider(name="Test")
    jp.save()
    person = Person(first_name="Max",last_name="Mustermann")
    person.full_clean()
    person.save()
    t = ContractType(id=1,build_method='pisa',template="",name=u'Art.60\xa77')
    t.save()
    job = Job(provider=jp,contract_type=t)
    #~ job = Job(contract_type=t,name="Test")
    job.save()
    n = Contract(id=1,job=job,user=root,person=person)
    n.full_clean()
    n.save()
    
    
    if 'en' in babel.AVAILABLE_LANGUAGES:
    
        url = '/api/jobs/Contract/1?an=print'
        response = self.client.get(url,REMOTE_USER='root',HTTP_ACCEPT_LANGUAGE='en')
        result = self.check_json_result(response,'success message alert')
        self.assertEqual(result['success'],False)
        self.assertEqual(result['alert'],True)
        self.assertEqual(
          result['message'],
          u"""\
Action "Print" failed for Job Contract "Job Contract#1 (Max MUSTERMANN)":
Invalid template '' configured for ContractType u'Art.60\\xa77' (expected filename ending with '.pisa.html').
An error report has been sent to the system administrator.""")

    
    #~ a = PrintAction()
    #~ from django.conf import settings
    #~ from django.utils.importlib import import_module
    #~ urls = import_module(settings.ROOT_URLCONF)
    #~ ui = urls.ui
    #~ try:
        #~ kw = a.run_(ui,n)
    #~ except Exception,e:
        #~ self.assertEqual(str(e),
          #~ u"Invalid template '' configured for ContractType u'Art.60\\xa77'. Expected filename ending with '.pisa.html'.")
          
          #~ u"Invalid template '' configured for ContractType u'Art.60\\xa77'. Expected filename ending with '.pisa.html'."
          
    #~ t.template='Default.odt'
    #~ t.save()
    #~ n = Contract.objects.get(id=1)
    #~ kw = a.run_(n)
    
    #~ print kw
    
    #~ response = self.client.get('/api/dsbe/Contracts/1?fmt=print',REMOTE_USER='root')
    #~ print response
    #~ result = self.check_json_result(response,'message success alert')
    #~ self.assertEqual(result['message'],'...')
    

    
def test02(self):
    """
    Testing whether `/api/notes/NoteTypes/1?fmt=json` 
    has no item `templateHidden`.
    Created :doc:`/blog/2011/0509`.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_tests.py`.
    """
    #~ from lino.apps.dsbe.models import NoteType
    from lino.modlib.notes.models import NoteType
    i = NoteType(build_method='appyodt',template="Default.odt",id=1)
    i.save()
    response = self.client.get('/api/notes/NoteTypes/1?fmt=json',REMOTE_USER='root')
    result = self.check_json_result(response,'data title navinfo disable_delete id disabled_actions')
    self.assertEqual(result['data']['template'],'Default.odt')
    self.assertEqual(result['data'].has_key('templateHidden'),False)
    
    response = self.client.get('/api/notes/NoteTypes/1?fmt=detail',REMOTE_USER='root')
    #~ print '\n'.join(response.content.splitlines()[:1])
    
    c = response.content
    
    #~ print c
    
    self.assertTrue(c.endswith('''\
<div id="body"></div>
</body></html>'''))

    if False:
        """
        TODO:
        expat has a problem to parse the HTML generated by Lino.
        Problem occurs near <div class="htmlText">...
        Note that even if the parseString gets through, we won't 
        have any INPUT elements since they will be added dynamically 
        by the JS code...
        """
        fd = file('tmp.html','w')
        fd.write(c)
        fd.close()
        
        from xml.dom import minidom 
        dom = minidom.parseString(c)
        print dom.getElementsByTagName('input')
        response = self.client.get('/api/lino/SiteConfigs/1?fmt=json')
        
        
def test04(self):
    """
    Test some features used in document templates.
    Created :doc:`/blog/2011/0615`.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_tests.py`.
    """
    if 'fr' in babel.AVAILABLE_LANGUAGES:
        from lino.apps.dsbe.models import Person, Company, Country, City
        from lino.utils.choicelists import Gender
        babel.set_language('fr')
        be = Country(isocode="BE",name="Belgique")
        be.save()
        bxl = City(name="Bruxelles",country=be)
        bxl.save()
        p = Person(
          first_name="Jean Louis",last_name="Dupont",
          street_prefix="Avenue de la", street="gare", street_no="3", street_box="b",
          city=bxl, gender=Gender.male
          )
        p.full_clean()
        p.save()
        #~ self.assertEqual(p.get_titled_name,"Mr Jean Louis DUPONT")
        self.assertEqual(p.full_name,"M. Jean Louis DUPONT")
        self.assertEqual('\n'.join(p.address_lines()),u"""\
M. Jean Louis DUPONT
Avenue de la gare 3 b
Bruxelles
Belgique""")
    
        if 'de' in babel.AVAILABLE_LANGUAGES:
            babel.set_language('de')
            self.assertEqual(p.full_name,"Herrn Jean Louis DUPONT")
            self.assertEqual(p.get_full_name(nominative=True),"Herr Jean Louis DUPONT")
            self.assertEqual(p.get_full_name(salutation=False),"Jean Louis DUPONT")
        
        babel.set_language(None)
        
        
        
def test05(self):
    """
    obj2str() caused a UnicodeDecodeError when called on an object that had 
    a ForeignKey field pointing to another instance whose __unicode__() 
    contained non-ascii characters.
    See :doc:`/blog/2011/0728`.
    """
    from lino.apps.dsbe.models import Activity, Person
    from lino.tools import obj2str
    a = Activity(name=u"Sozialhilfeempfänger")
    p = Person(last_name="Test",activity=a)
    self.assertEqual(unicode(a),u"Sozialhilfeempfänger")
    
    # Django pitfall: repr() of a model instance may return basestring containing non-ascii characters.
    self.assertEqual(type(repr(a)),str)

    # 
    self.assertEqual(obj2str(a,True),"Activity(name=u'Sozialhilfeempf\\xe4nger')")
    a.save()
    self.assertEqual(obj2str(a,True),u"Activity(id=1,name=u'Sozialhilfeempf\\xe4nger')")
    
    expected = "Person(language=u'%s'," % babel.DEFAULT_LANGUAGE
    expected += "last_name='Test',"
    expected += "is_active=True"
    #~ expected += r",activity=Activity(name=u'Sozialhilfeempf\xe4nger'))"
    #~ expected += ",activity=1"
    expected += ")"
    self.assertEqual(obj2str(p,True),expected)
    p.pk = 5
    self.assertEqual(obj2str(p),"Person #5 (u'TEST  (5)')")
    
    
def test06(self):
    """
    :doc:`/blog/2011/1003`.
    The `id` field of a Company or Person was never disabled 
    because Lino didn't recognize it as the primary key.
    
    """
    from django.db import models
    from lino.apps.dsbe.models import Person
    from lino.core.coretools import get_data_elem
    de = get_data_elem(Person,'id')
    #~ print de.__class__
    self.assertEqual(de.__class__,models.AutoField)
    self.assertEqual(de.primary_key,True)
    pk = Person._meta.pk
    self.assertEqual(pk.__class__,models.OneToOneField)
    self.assertEqual(pk.primary_key,True)
    self.assertEqual(pk.rel.field_name,'id')
    
    #~ self.assertEqual(de,pk)
    

def test07(self):
    """
    Bug 20120127 : VirtualFields had sneaked into wildcard columns.
    """
    from lino.apps.dsbe.models import Companies
    wcde = [de.name for de in Companies.wildcard_data_elems()]
    expected = '''\
id country city name addr1 street_prefix street street_no street_box 
addr2 zip_code region language email url phone gsm fax remarks 
contact_ptr vat_id type is_active newcomer is_deprecated activity 
bank_account1 bank_account2 prefix hourly_rate'''.split()
    
    s = ' '.join(wcde)
    #~ print s
    #~ print [de for de in Companies.wildcard_data_elems()]
    self.assertEqual(wcde,expected)
        
