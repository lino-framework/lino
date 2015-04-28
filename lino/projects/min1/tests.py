# -*- coding: utf-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This module contains some relatively quick tests that don't load any
fixtures.

To run only this test::

  $ go min1
  $ manage.py test contacts.QuickTest

"""

from __future__ import unicode_literals

from django.conf import settings
from django.utils import translation

from lino.utils.djangotest import RemoteAuthTestCase

from lino.api import dd, rt

from lino.utils.instantiator import create_and_get

from lino.modlib.contacts import models as contacts
from lino.modlib.users.choicelists import UserProfiles

Genders = dd.Genders


class QuickTest(RemoteAuthTestCase):

    def test01(self):
        """
        Tests some basic funtionality.
        """
        self.assertEqual(
            settings.MIDDLEWARE_CLASSES, (
                'django.middleware.common.CommonMiddleware',
                'django.middleware.locale.LocaleMiddleware',
                'lino.core.auth.RemoteUserMiddleware',
                'lino.utils.ajax.AjaxExceptionResponse'))

        Person = dd.resolve_model("contacts.Person")

        ee = create_and_get('countries.Country',
                            isocode='EE', **dd.babelkw('name',
                                                    de="Estland",
                                                    fr='Estonie',
                                                    en="Estonia",
                                                    nl='Estland',
                                                    et='Eesti',
                                                    ))
        be = create_and_get('countries.Country',
                            isocode='BE', **dd.babelkw('name',
                                                    de="Belgien",
                                                    fr='Belgique',
                                                    en="Belgium",
                                                    nl='Belgie',
                                                    et='Belgia',
                                                    ))

        PlaceTypes = rt.modules.countries.PlaceTypes
        eupen = create_and_get(
            'countries.Place', name=u'Eupen', country=be, zip_code='4700')

        vigala = create_and_get('countries.Place',
                                name='Vigala',
                                country=ee,
                                type=PlaceTypes.municipality)

        luc = create_and_get(Person,
                             first_name='Luc', last_name='Saffre',
                             gender=Genders.male,
                             country=ee, street='Uus', street_no='1',
                             addr2=u'Vana-Vigala küla',
                             city=vigala, zip_code='78003')

        settings.SITE.uppercase_last_name = True

        """If the following tests raise a "DoesNotExist: Company matching
        query does not exist" then this may come because
        Site._site_config has been filled before the database switched
        from the real db to test db.  and not properly reset.

        """

        with translation.override('en'):
            self.assertEquals(luc.address, u'''\
Mr Luc SAFFRE
Uus 1
Vana-Vigala küla
78003 Vigala vald
Estonia''')

        with translation.override('de'):
            self.assertEquals(luc.address, u'''\
Herrn Luc SAFFRE
Uus 1
Vana-Vigala küla
78003 Vigala vald
Estland''')
            self.assertEquals(luc.address_html, '''\
<p>Herrn Luc SAFFRE<br />Uus 1<br />Vana-Vigala k&#252;la<br />78003 Vigala vald<br />Estland</p>''')

        # "new" or "full" style is when the database knows the
        # geographic hierarchy. We then just select "Vana-Vigala" as
        # the "City".

        vana_vigala = create_and_get('countries.Place',
                                     name='Vana-Vigala',
                                     country=ee,
                                     parent=vigala,
                                     type=PlaceTypes.village,
                                     zip_code='78003')

        meeli = create_and_get(Person,
                               first_name='Meeli', last_name='Mets',
                               gender=Genders.female,
                               country=ee, street='Hirvepargi',
                               street_no='123',
                               city=vana_vigala)

        with translation.override('en'):
            self.assertEquals(meeli.address, u'''\
Mrs Meeli METS
Hirvepargi 123
Vana-Vigala küla
78003 Vigala vald
Estonia''')

        u = create_and_get(settings.SITE.user_model,
                           username='root', language='',
                           profile=UserProfiles.admin)

        """
        disable SITE.is_imported_partner() otherwise 
        disabled_fields may contain more than just the 'id' field.
        """
        save_iip = settings.SITE.is_imported_partner

        def f(obj):
            return False
        settings.SITE.is_imported_partner = f

        """
        Note that we must specify the language both in the user 
        and in HTTP_ACCEPT_LANGUAGE because...
        """

        luc = Person.objects.get(name__exact="Saffre Luc")
        self.assertEqual(luc.pk, contacts.PARTNER_NUMBERS_START_AT)

        url = settings.SITE.buildurl(
            'api', 'contacts', 'Person',
            '%d?query=&an=detail&fmt=json' % luc.pk)
        #~ url = '/api/contacts/Person/%d?query=&an=detail&fmt=json' % luc.pk
        if settings.SITE.get_language_info('en'):
            u.language = 'en'
            u.save()
            response = self.client.get(
                url, REMOTE_USER='root', HTTP_ACCEPT_LANGUAGE='en')
            result = self.check_json_result(
                response, 'navinfo disable_delete data id title')
            self.assertEqual(result['data']['country'], "Estonia")
            self.assertEqual(result['data']['gender'], "Male")

        if settings.SITE.get_language_info('de'):
            u.language = 'de'
            u.save()
            response = self.client.get(
                url, REMOTE_USER='root', HTTP_ACCEPT_LANGUAGE='de')
            result = self.check_json_result(
                response,
                'navinfo disable_delete data id title')
            self.assertEqual(result['data']['country'], "Estland")
            self.assertEqual(result['data']['gender'], u"Männlich")
            #~ self.assertEqual(result['data']['disabled_fields'],['contact_ptr_id','id'])
            #~ self.assertEqual(result['data']['disabled_fields'],['id'])
            df = result['data']['disabled_fields']
            self.assertEqual(df['id'], True)

        if settings.SITE.get_language_info('fr'):
            u.language = 'fr'
            u.save()
            response = self.client.get(
                url, REMOTE_USER='root', HTTP_ACCEPT_LANGUAGE='fr')
            result = self.check_json_result(
                response, 'navinfo disable_delete data id title')
            self.assertEqual(result['data']['country'], "Estonie")
            self.assertEqual(result['data']['gender'], u"Masculin")

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
        elem = SiteConfigs.get_row_by_pk(None, settings.SITE.config_id)
        self.assertEqual(elem.next_partner_id,
                         contacts.PARTNER_NUMBERS_START_AT + 2)

        elem.next_partner_id = 12345
        elem.full_clean()
        elem.save()
        #~ print "saved"
        self.assertEqual(settings.SITE.site_config.next_partner_id, 12345)
        john = create_and_get(Person, first_name='John', last_name='Smith')
        self.assertEqual(john.pk, 12345)
        self.assertEqual(elem.next_partner_id, 12346)
        self.assertEqual(settings.SITE.site_config.next_partner_id, 12346)

    def unused_test03(self):
        """
        Test the following situation:

        - User 1 opens the :menuselection:`Configure --> System--> System Parameters` dialog
        - User 2 creates a new Person (which increases next_partner_id)
        - User 1 clicks on `Save`.

        `next_partner_id` may not get overwritten

        """

        url = settings.SITE.buildurl(
            'api', 'system', 'SiteConfigs', '1?an=detail&fmt=json')
        response = self.client.get(url, REMOTE_USER='root')
        result = self.check_json_result(
            response, 'navinfo disable_delete data id title')
        """
        `test01` created one Person, so next_partner_id should be at 101:
        """
        data = result['data']
        self.assertEqual(data['next_partner_id'],
                         contacts.PARTNER_NUMBERS_START_AT + 1)

        data['next_partner_id'] = 12345
        #~ pprint(data)
        response = self.client.put(
            url, data,
            #~ content_type="application/x-www-form-urlencoded; charset=UTF-8",
            REMOTE_USER='root')

        result = self.check_json_result(
            response, 'message rows success data_record')
        data = result['data_record']['data']

        john = create_and_get(Person, first_name='John', last_name='Smith')
        # fails: self.assertEqual(john.pk,12345)

    def test02(self):
        # This case demonstratest that ordering does not ignore case, at
        # least in sqlite. we would prefer to have `['adams', 'Zybulka']`,
        # but we get `['Zybulka', 'adams']`.

        contacts = rt.modules.contacts
        contacts.Partner(name="Zybulka").save()
        contacts.Partner(name="adams").save()
        ar = rt.login().spawn(contacts.Partners)
        l = [p.name for p in ar]
        expected = ['Zybulka', 'adams']
        self.assertEqual(l, expected)

