# -*- coding: utf-8 -*-
## Copyright 2011 Luc Saffre
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
This module contains tests that are run on a demo database
with the following fixtures:

  std all_countries few_cities all_languages props demo
  
"""

import logging
logger = logging.getLogger(__name__)

from django.db.utils import IntegrityError
from django.conf import settings
from django.utils.encoding import force_unicode

#~ from django.utils import unittest
#~ from django.test.client import Client
#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country

from lino.utils import i2d
from lino.utils import babel
from lino.tools import resolve_model
#Companies = resolve_model('contacts.Companies')
from lino.utils.test import TestCase


#~ Person = resolve_model('contacts.Person')
#~ Property = resolve_model('properties.Property')
#~ PersonProperty = resolve_model('properties.PersonProperty')

class DemoTest(TestCase):
    #~ fixtures = [ 'std','demo' ]
    fixtures = 'std few_countries few_cities few_languages props demo'.split()
    #~ fixtures = 'std all_countries few_cities all_languages props demo'.split()
    
    #~ def setUp(self):
        #~ settings.LINO.auto_makeui = False
        #~ super(DemoTest,self).setUp()
    
            
def test01(self):
    """
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_demo_tests.py`.
    """
    from lino.apps.dsbe.models import Person
    self.assertEquals(Person.objects.count(), 73)
    
    p = Person.objects.get(pk=118)
    self.assertEquals(unicode(p), "Annette ARENS (118)")
    
    
        
def test02(self):
    """
    This tests for the bug discovered :doc:`/blog/2011/0228`.
    See also :doc:`/blog/2011/0531`.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_demo_tests.py`.
    """
    url = '/api/dsbe/SoftSkillsByPerson?mt=22&mk=118&fmt=json'
    # make sure that the response is in English so that this test works on any site
    #~ 20111111 babel.set_language('en')
    #~ extra = {'Accept-Language':'fr,de-DE;q=0.8,de;q=0.6,en-US;q=0.4,en;q=0.2'
    #~ extra = {'Accept-Language':'en-US'}
    #~ extra = dict(REMOTE_USER='root')
    #~ from django.conf import settings
    #~ babel.DEFAULT_LANGUAGE = 'en'
    #~ settings.LANGUAGE = 'en'
    if 'en' in babel.AVAILABLE_LANGUAGES:
        response = self.client.get(url,REMOTE_USER='root',HTTP_ACCEPT_LANGUAGE='en')
        result = self.check_json_result(response,'count rows gc_choices title')
        self.assertEqual(result['title'],"Properties of Annette ARENS (118)")
        self.assertEqual(len(result['rows']),3)
        row = result['rows'][0]
        self.assertEqual(row[0],"Obedient")
        self.assertEqual(row[1],7)
        self.assertEqual(row[2],"moderate")
        self.assertEqual(row[3],"2")
        
    if 'de' in babel.AVAILABLE_LANGUAGES:
        response = self.client.get(url,REMOTE_USER='root',HTTP_ACCEPT_LANGUAGE='de')
        result = self.check_json_result(response,'count rows gc_choices title')
        self.assertEqual(result['title'],"Eigenschaften von Annette ARENS (118)")
        self.assertEqual(len(result['rows']),3)
        row = result['rows'][0]
        self.assertEqual(row[0],"Gehorsam")
        #~ self.assertEqual(row[0],"Gehorsam")
        self.assertEqual(row[1],7)
        self.assertEqual(row[2],u"mittelmäßig")
        self.assertEqual(row[3],"2")
        
    #~ 20111111 babel.set_language(None) # switch back to default language for subsequent tests
    
    #~ tf('http://127.0.0.1:8000/api/properties/SoftSkillsByPerson?_dc=1298881440121&fmt=json&mt=22&mk=15',
        #~ """
        #~ { 
        #~ count: 3, 
        #~ rows: [ 
          #~ [ "Gehorsam", 7, "mittelm\u00e4\u00dfig", "2", null, 53, "Sozialkompetenzen", 2 ], 
          #~ [ "F\u00fchrungsf\u00e4higkeit", 8, "mittelm\u00e4\u00dfig", "2", null, 54, "Sozialkompetenzen", 2 ], 
          #~ [ null, null, null, null, null, null, "Sozialkompetenzen", 2 ] 
        #~ ], 
        #~ gc_choices: [  ], 
        #~ title: "~Eigenschaften pro Person Arens Annette (15)" 
        #~ }
        #~ """)
    


def test03(self):
    """
    Test whether the AJAX call issued for Detail of Annette Arens is correct.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_demo_tests.py`.
    
    The raw call looks like this::
    
      {
          "navinfo": {
              "last": 93,
              "recno": 3,
              "prev": 14,
              "message": "Record  3 von 73",
              "first": 16,
              "next": 68
          },
          "disable_delete": "Aus TIM importierte Partner d\u00fcrfen nicht gel\u00f6scht werden.",
          "data": {
              "last_name": "Arens",
              "street_box": "",
              "residence_permit": "[<a href=\"javascript:Lino.uploads.UploadsByPerson.insert(undefined,{ &quot;data_record&quot;: { &quot;data&quot;: { &quot;delay_value&quot;: 0, &quot;description&quot;: null, &quot;created&quot;: null, &quot;reminder_date&quot;: null, &quot;company&quot;: null, &quot;modified&quot;: null, &quot;typeHidden&quot;: 2, &quot;personHidden&quot;: 15, &quot;companyHidden&quot;: null, &quot;person&quot;: &quot;Arens Annette (15)&quot;, &quot;delay_type&quot;: &quot;Tage&quot;, &quot;delay_typeHidden&quot;: &quot;D&quot;, &quot;file&quot;: &quot;&quot;, &quot;reminder_text&quot;: null, &quot;type&quot;: &quot;Aufenthaltserlaubnis&quot;, &quot;id&quot;: null } } })\">Upload</a>]",
              "work_permit": "[<a href=\"javascript:Lino.uploads.UploadsByPerson.insert(undefined,{ &quot;data_record&quot;: { &quot;data&quot;: { &quot;delay_value&quot;: 0, &quot;description&quot;: null, &quot;created&quot;: null, &quot;reminder_date&quot;: null, &quot;company&quot;: null, &quot;modified&quot;: null, &quot;typeHidden&quot;: 3, &quot;personHidden&quot;: 15, &quot;companyHidden&quot;: null, &quot;person&quot;: &quot;Arens Annette (15)&quot;, &quot;delay_type&quot;: &quot;Tage&quot;, &quot;delay_typeHidden&quot;: &quot;D&quot;, &quot;file&quot;: &quot;&quot;, &quot;reminder_text&quot;: null, &quot;type&quot;: &quot;Arbeitserlaubnis&quot;, &quot;id&quot;: null } } })\">Upload</a>]",
              "cityHidden": 1,
              "addr2": "",
              "birth_country": "Belgien",
              "unemployed_since": null,
              "genderHidden": null,
              "group": null,
              "title": "",
              "civil_state": null,
              "fax": "",
              "is_active": true,
              "coached_until": null,
              "coach1Hidden": null,
              "job_office_contact": null,
              "income_ag": false,
              "skills": null,
              "civil_stateHidden": null,
              "coach2Hidden": null,
              "unavailable_until": null,
              "is_seeking": false,
              "activity": null,
              "gender": null,
              "street": "Akazienweg",
              "first_name": "Annette",
              "coached_from": null,
              "is_cpas": true,
              "disabled_fields": ["name", "first_name", "last_name", "title", "remarks", "zip_code", "city", "country", "street", "street_no", "street_box", "birth_date", "gender", "birth_place", "coach1", "language", "phone", "fax", "email", "card_number", "card_valid_from", "card_valid_until", "noble_condition", "card_issuer", "national_id", "health_insurance", "pharmacy", "bank_account1", "bank_account2", "gesdos_id", "activity", "is_cpas", "is_senior", "is_active", "nationality", "id"],
              "email": null,
              "zip_code": "4700",
              "LinksByPerson": "<a href=\"/api/links/LinksByOwnerBase/4?fmt=detail\" target=\"_blank\">Python website</a><br><a href=\"/api/links/LinksByOwnerBase/5?fmt=detail\" target=\"_blank\">Google</a><br><a href=\"/api/links/LinksByOwnerBase/6?fmt=detail\" target=\"_blank\">Lino website</a><br><a href=\"/api/links/LinksByOwnerBase/7?fmt=detail\" target=\"_blank\">Django website</a>",
              "income_kg": false,
              "birth_date_circa": false,
              "nationalityHidden": "BE",
              "native_language": "Deutsch",
              "nationality": "Belgien",
              "work_permit_suspended_until": null,
              "unavailable_why": null,
              "aid_type": null,
              "country": "Belgien",
              "card_valid_from": null,
              "job_office_contactHidden": null,
              "income_rente": false,
              "overview": "Sprachkenntnisse: <b>nicht ausgef\u00fcllt</b><br/>Ausbildung: <b>nicht ausgef\u00fcllt</b><br/>Contracts: <b>nicht ausgef\u00fcllt</b>",
              "health_insuranceHidden": null,
              "health_insurance": null,
              "birth_place": null,
              "city": "Eupen",
              "aid_typeHidden": null,
              "groupHidden": null,
              "in_belgium_since": null,
              "income_misc": false,
              "UploadsByPerson": "",
              "bank_account1": null,
              "phone": "",
              "language": "German",
              "card_valid_until": null,
              "needs_residence_permit": false,
              "card_type_text": null,
              "card_number": null,
              "is_senior": false,
              "needs_work_permit": false,
              "languageHidden": "de",
              "national_id": "",
              "countryHidden": "BE",
              "gesdos_id": null,
              "birth_countryHidden": "BE",
              "id": 15,
              "coach1": null,
              "coach2": null,
              "activityHidden": null,
              "bank_account2": null,
              "job_agents": null,
              "residence_typeHidden": null,
              "street_no": "",
              "driving_licence": "[<a href=\"javascript:Lino.uploads.UploadsByPerson.insert(undefined,{ &quot;data_record&quot;: { &quot;data&quot;: { &quot;delay_value&quot;: 0, &quot;description&quot;: null, &quot;created&quot;: null, &quot;reminder_date&quot;: null, &quot;company&quot;: null, &quot;modified&quot;: null, &quot;typeHidden&quot;: null, &quot;personHidden&quot;: 15, &quot;companyHidden&quot;: null, &quot;person&quot;: &quot;Arens Annette (15)&quot;, &quot;delay_type&quot;: &quot;Tage&quot;, &quot;delay_typeHidden&quot;: &quot;D&quot;, &quot;file&quot;: &quot;&quot;, &quot;reminder_text&quot;: null, &quot;type&quot;: null, &quot;id&quot;: null } } })\">Upload</a>]",
              "noble_condition": null,
              "card_issuer": null,
              "income_wg": false,
              "remarks": null,
              "native_languageHidden": "ger",
              "residence_type": null,
              "age": "unbekannt",
              "obstacles": null,
              "birth_date": null,
              "gsm": ""
          },
          "id": 15,
          "title": "Arens Annette (15)"
      }        
    
    
    """
    # 
    response = self.client.get('/api/contacts/Persons/117?fmt=json',REMOTE_USER='root')
    result = self.check_json_result(response,'navinfo disable_delete data id title disabled_actions')
    #~ result = simplejson.loads(response.content)
    #~ for k in 'navinfo disable_delete data id title'.split():
        #~ self.assertTrue(result.has_key(k))
    if False:
        # disabled because they depend on local database sorting configuration
        self.assertEqual(result['navinfo']['last'],93)
        self.assertEqual(result['navinfo']['recno'],3)
        self.assertEqual(result['navinfo']['prev'],14)
        self.assertEqual(result['navinfo']['first'],16)
        self.assertEqual(result['navinfo']['next'],68)
    self.assertEqual(result['data']['last_name'],"Arens")
    self.assertEqual(result['data']['first_name'],"Andreas")
            
            
def test04(self):
    """
    This tests whether date fields are correctly parsed.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_demo_tests.py`.
    
    ::
    
      {
        "navinfo": {
            "last": 2,
            "recno": 1,
            "prev": null,
            "message": "Record  1 von 2",
            "first": 1,
            "next": 2
        },
        "disable_delete": null,
        "data": {
            "user_asdHidden": null,
            "date_ended": null,
            "languageHidden": "de",
            "duties_company": null,
            "ending": null,
            "duties_asd": null,
            "exam_policyHidden": null,
            "duration": null,
            "id": 1,
            "regime": null,
            "applies_from": '01.03.2010',
            "refund_rate": null,
            "endingHidden": null,
            "userHidden": 4,
            "responsibilities": null,
            "personHidden": 16,
            "delay_type": "Tage",
            "reminder_text": "demo reminder",
            "hourly_rate": null,
            "type": "Konvention Art.60\u00a77 Sozial\u00f6konomie",
            "schedule": null,
            "reminder_date": '11.11.2010',
            "company": "R-Cycle Sperrgutsortierzentrum",
            "date_issued": null,
            "contactHidden": 2,
            "exam_policy": null,
            "applies_until": '17.05.2009',
            "user_asd": null,
            "user": "root",
            "reference_person": null,
            "delay_value": 0,
            "companyHidden": 83,
            "disabled_fields": ["id"],
            "language": "Deutsch",
            "typeHidden": 1,
            "person": "Altenberg Hans (16)",
            "contact": "Arens Andreas (14) (Gesch\u00e4ftsf\u00fchrer)",
            "delay_typeHidden": "D",
            "goals": null,
            "duties_dsbe": null,
            "stages": null,
            "date_decided": null
        },
        "id": 1,
        "title": "Vertrag Nr. 1"
      }
    """
    for value in ('01.03.2011','15.03.2011'):
        url ='/api/jobs/Contracts/1'
        data =  'applies_from='+value+'&applies_until=17.05.2009&company=R-Cycle%20'
        'Sperrgutsortierzentrum&companyHidden=83&contact=Arens%20Andreas%20(1'
        '4)%20(Gesch%C3%A4ftsf%C3%BChrer)&contactHidden=2&date_decided=&date_e'
        'nded=&date_issued=&delay_type=Tage&delay_typeHidden=D&delay_value=0&du'
        'ration=&ending=Vertragsbeendigung%20ausw%C3%A4hlen...&endingHidden=&lan'
        'guage=Deutsch&languageHidden=de&person=Altenberg%20Hans%20(16)&personHi'
        'dden=16&reminder_date=11.11.2010&reminder_text=demo%20reminder&type=Kon'
        'vention%20Art.60%C2%A77%20Sozial%C3%B6konomie&typeHidden=1&user=root&us'
        'erHidden=4&user_asd=Benutzer%20ausw%C3%A4hlen...&user_asdHidden='
        
        response = self.request_PUT(url,data,REMOTE_USER='root')
        result = self.check_json_result(response,'message success')
        self.assertEqual(result['success'],True)
        
        url = "/api/jobs/Contracts/1?fmt=json"
        response = self.client.get(url,REMOTE_USER='root')
        #~ print 20110723, response
        result = self.check_json_result(response,'navinfo disable_delete data id title disabled_actions')
        self.assertEqual(result['data']['applies_from'],value)

def test05(self):
    """
    Simplification of test04, used to write :doc:`/tickets/27`.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_demo_tests.py`.
    """
    url ='/api/countries/Countries/BE'
    data = 'name=Belgienx&nameHidden=Belgienx&fmt=json'
    response = self.request_PUT(url,data,REMOTE_USER='root')
    #~ response = self.client.put(url,data,content_type='application/x-www-form-urlencoded')
    result = self.check_json_result(response,'message success')
    self.assertEqual(result['success'],True)
    
    url ='/api/countries/Countries/BE?fmt=json'
    response = self.client.get(url,REMOTE_USER='root')
    result = self.check_json_result(response,'navinfo disable_delete data id title disabled_actions')
    self.assertEqual(result['data']['name'],'Belgienx')


def test06(self):
    """
    Testing BabelValues.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_demo_tests.py`.
    """
    from lino.utils import babel
    from lino.apps.dsbe.models import Person
    from lino.apps.dsbe.models import Property, PersonProperty
    annette = Person.objects.get(pk=118)
    self.assertEquals(unicode(annette), "Annette ARENS (118)")
    
    babel.set_language('en')
    p = Property.objects.get(name_en="Obedient")
    pp = PersonProperty.objects.get(person=annette,property__name_en="Obedient")
        
    if 'de' in babel.AVAILABLE_LANGUAGES:
        babel.set_language('de')
        self.assertEquals(unicode(p), u"Gehorsam")
        self.assertEquals(unicode(pp), u"mittelmäßig")
        #~ self.assertEquals(unicode(pp), u"Sozialkompetenzen.Gehorsam=mittelmäßig")
    
    if 'fr' in babel.AVAILABLE_LANGUAGES:
        babel.set_language('fr')
        self.assertEquals(unicode(p), u"Obéissant")
        #~ self.assertEquals(unicode(pp), u"Compétences sociales.Obéissant=moyennement")
        self.assertEquals(unicode(pp), u"moyennement")
    
    #~ babel.set_language(babel.DEFAULT_LANGUAGE)
    babel.set_language(None) # switch back to default language for subsequent tests
    
def test07(self):
    """
    Testing whether all model reports work
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_demo_tests.py`.
    """
    response = self.client.get('/menu',REMOTE_USER='root')
    result = self.check_json_result(response,'success message load_menu')
    self.assertEqual(result['load_menu']['name'],'...')
test07.skip = "Doesn't work because simplejson.loads() doesn't parse functions"


def test08(self):
    """
    In `MyPersons` wurden seit :doc:`/blog/2011/0408` zu viele Leute angezeigt: 
    auch die, die weder Anfangs- noch Enddatum haben. 
    Damit jemand als begleitet gilt, muss mindestens eines der 
    beiden Daten ausgefüllt sein.
    
    See :doc:`/blog/2011/0412`
    """
    from lino.apps.dsbe.models import Person, MyPersons, only_coached_persons,only_my_persons
    from lino.modlib.users.models import User
    u = User.objects.get(username='root')
    #~ qs = Person.objects.order_by('last_name','first_name')
    qs = Person.objects.order_by('id')
    #~ print "Person.object.all()", qs
    qs = only_my_persons(qs,u)
    #~ print "only_my_persons()", qs
    self.assertEqual(qs.count(),4)
    qs = only_coached_persons(qs,i2d(20100901))
    #~ print "only_coached_persons(20100901)", qs
    self.assertEqual(qs.count(),3)
    #~ qs = MyPersons.request(user=)
    l = [unicode(p) for p in qs]
    
    self.assertEqual(l,[u"Laurent BASTIAENSEN (121)",
        u'Erna ÄRGERLICH (171)',u"Emil EIERSCHAL (177)"])
    
    
def test09(self):
    """
    This tests for the bug discovered :doc:`/blog/2011/0610`.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_demo_tests.py`.
    """
    #~ babel.set_language('en')
    url = '/choices/jobs/StudiesByPerson/city?start=0&limit=30&country=&query='
    response = self.client.get(url,REMOTE_USER='root')
    result = self.check_json_result(response,'count rows')
    #~ self.assertEqual(result['title'],u"Choices for city")
    self.assertEqual(len(result['rows']),30)
    #~ babel.set_language(None) # switch back to default language for subsequent tests

def test10(self):
    """
    Test the unique_together validation of City
    See :doc:`/blog/2011/0610` and :doc:`/blog/2011/0611`.
    See the source code at :srcref:`/lino/apps/dsbe/tests/dsbe_demo_tests.py`.
    """
    from lino.modlib.countries.models import City, Country
    be = Country.objects.get(pk='BE')
    try:
        City(name="Eupen",country=be,zip_code='4700').save()
    except IntegrityError:
        if settings.LINO.allow_duplicate_cities:
            self.fail("Got IntegrityError though allow_duplicate_cities should be allowed.")
    else:
        if not settings.LINO.allow_duplicate_cities:
            self.fail("Expected IntegrityError")
        
    
    try:
        be.city_set.create(name="Eupen",zip_code='4700')
    except IntegrityError:
        if settings.LINO.allow_duplicate_cities:
            self.fail("Got IntegrityError though allow_duplicate_cities should be allowed.")
    else:
        if not settings.LINO.allow_duplicate_cities:
            self.fail("Expected IntegrityError")
        
    
