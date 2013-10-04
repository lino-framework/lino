# -*- coding: utf-8 -*-
## Copyright 2008-2013 Luc Saffre
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
This module contains some relatively quick tests 
that don't load any fixtures.

To run only this test::

  manage.py test contacts.QuickTest
  
"""

from __future__ import unicode_literals

from pprint import pprint

from django.conf import settings
from django.utils import translation

from djangosite.utils.djangotest import RemoteAuthTestCase
from django.test.utils import override_settings

#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
from north import dbutils

from lino import dd
Person = dd.resolve_model("contacts.Person")
from lino.utils.instantiator import Instantiator, create_and_get
from north.dbutils import babelkw

from lino.modlib.contacts import models as contacts

from lino import mixins
Genders = mixins.Genders

person = Instantiator(Person).build
company = Instantiator("contacts.Company").build

class QuickTest(RemoteAuthTestCase):
    
    def test01(self):
        """
        Tests some basic funtionality.
        """
        #~ self.assertEqual(settings.MIDDLEWARE_CLASSES,1)
        
        ee = create_and_get('countries.Country',
            isocode='EE',**babelkw('name',
            de="Estland",
            fr='Estonie',
            en="Estonia",
            nl='Estland',
            et='Eesti',
            ))
        be = create_and_get('countries.Country',
            isocode='BE',**babelkw('name',
            de="Belgien",
            fr='Belgique',
            en="Belgium",
            nl='Belgie',
            et='Belgia',
            ))
            
        eupen = create_and_get('countries.City',name=u'Eupen',country=be,zip_code='4700')
            
        vigala = create_and_get('countries.City',name=u'Vigala',country=ee)
        
        luc = create_and_get(Person,
            first_name='Luc',last_name='Saffre',
            gender=Genders.male,
            country=ee,street='Uus', street_no='1',
            addr2=u'Vana-Vigala küla',
            city=vigala,zip_code='78003')
            
        settings.SITE.uppercase_last_name = True
        
        """
        If the following tests raise a
        "DoesNotExist: Company matching query does not exist"
        then this may come because Site._site_config has been 
        filled before the database switched from the real db to test db.
        and not properly reset.
        """
        
        if settings.SITE.get_language_info('en'):
          with translation.override('en'):
            #~ dbutils.set_language('en')
            self.assertEquals(luc.address, u'''\
Mr Luc SAFFRE
Uus 1
Vana-Vigala küla
78003 Vigala
Estonia''')

        if settings.SITE.get_language_info('de'):
            with translation.override('de'):
                self.assertEquals(luc.address, u'''\
Herrn Luc SAFFRE
Uus 1
Vana-Vigala küla
78003 Vigala
Estland''')
                self.assertEquals(luc.address_html, '''\
<p>Herrn Luc SAFFRE<br />Uus 1<br />Vana-Vigala k&#252;la<br />78003 Vigala<br />Estland</p>''')
            
        u = create_and_get(settings.SITE.user_model,
            username='root',language='',profile=dd.UserProfiles.admin)
            
        
        """
        disable SITE.is_imported_partner() otherwise 
        disabled_fields may contain more than just the 'id' field.
        """
        save_iip = settings.SITE.is_imported_partner
        def f(obj): return False
        settings.SITE.is_imported_partner = f
        
        """
        Note that we must specify the language both in the user 
        and in HTTP_ACCEPT_LANGUAGE because...
        """
        
        luc = Person.objects.get(name__exact="Saffre Luc")
        self.assertEqual(luc.pk,contacts.PARTNER_NUMBERS_START_AT)
        
        url = settings.SITE.build_admin_url('api','contacts','Person','%d?query=&an=detail&fmt=json' % luc.pk)
        #~ url = '/api/contacts/Person/%d?query=&an=detail&fmt=json' % luc.pk
        if settings.SITE.get_language_info('en'):
            u.language = 'en'
            u.save()
            response = self.client.get(url,REMOTE_USER='root',HTTP_ACCEPT_LANGUAGE='en')
            result = self.check_json_result(response,'navinfo disable_delete data id title')
            self.assertEqual(result['data']['country'],"Estonia")
            self.assertEqual(result['data']['gender'],"Male")
        
        if settings.SITE.get_language_info('de'):
            u.language = 'de'
            u.save()
            response = self.client.get(url,REMOTE_USER='root',HTTP_ACCEPT_LANGUAGE='de')
            result = self.check_json_result(
              response,
              'navinfo disable_delete data id title')
            self.assertEqual(result['data']['country'],"Estland")
            self.assertEqual(result['data']['gender'],u"Männlich")
            #~ self.assertEqual(result['data']['disabled_fields'],['contact_ptr_id','id'])
            #~ self.assertEqual(result['data']['disabled_fields'],['id'])
            df = result['data']['disabled_fields']
            self.assertEqual(df['id'],True)
            
            
        if settings.SITE.get_language_info('fr'):
            u.language = 'fr'
            u.save()
            response = self.client.get(url,REMOTE_USER='root',HTTP_ACCEPT_LANGUAGE='fr')
            result = self.check_json_result(response,'navinfo disable_delete data id title')
            self.assertEqual(result['data']['country'],"Estonie")
            self.assertEqual(result['data']['gender'],u"Masculin")
            
        #~ u.language = lang
        #~ u.save()
        # restore is_imported_partner method
        settings.SITE.is_imported_partner = save_iip

        #~ def test03(self):
        """
        Test the following situation:
        
        - User 1 opens the :menuselection:`Configure --> System--> System Parameters` dialog
        - User 2 creates a new Person (which increases next_partner_id)
        - User 1 clicks on `Save`.
        
        `next_partner_id` may not get overwritten 
        
        """
        # User 1
        SiteConfigs = settings.SITE.modules.system.SiteConfigs
        elem = SiteConfigs.get_row_by_pk(None,settings.SITE.config_id)
        self.assertEqual(elem.next_partner_id,contacts.PARTNER_NUMBERS_START_AT + 1) 
        
        elem.next_partner_id = 12345
        elem.full_clean()
        elem.save()
        #~ print "saved"
        self.assertEqual(settings.SITE.site_config.next_partner_id,12345)
        john = create_and_get(Person,first_name='John',last_name='Smith')
        self.assertEqual(john.pk,12345)
        self.assertEqual(elem.next_partner_id,12346)
        self.assertEqual(settings.SITE.site_config.next_partner_id,12346)
        
        
    def unused_test03(self):
        """
        Test the following situation:
        
        - User 1 opens the :menuselection:`Configure --> System--> System Parameters` dialog
        - User 2 creates a new Person (which increases next_partner_id)
        - User 1 clicks on `Save`.
        
        `next_partner_id` may not get overwritten 
        
        """
        
        url = settings.SITE.build_admin_url('api','system','SiteConfigs','1?an=detail&fmt=json')
        response = self.client.get(url,REMOTE_USER='root')
        result = self.check_json_result(response,'navinfo disable_delete data id title')
        """
        `test01` created one Person, so next_partner_id should be at 101:
        """
        data = result['data']
        self.assertEqual(data['next_partner_id'],contacts.PARTNER_NUMBERS_START_AT + 1) 
        
        
        data['next_partner_id'] = 12345
        #~ pprint(data)
        response = self.client.put(url,data,
          #~ content_type="application/x-www-form-urlencoded; charset=UTF-8",
          REMOTE_USER='root')
        
        result = self.check_json_result(response,'message rows success data_record')
        data = result['data_record']['data']
        
        john = create_and_get(Person,first_name='John',last_name='Smith')
        # fails: self.assertEqual(john.pk,12345)
        """
        I no longer understand how to call test.Client.put() with normal form data...
        Furthermore this seems to change between 1.4 and 1.5, so I'll wait until all 
        my users have moved to 1.5.
        """
        

        
