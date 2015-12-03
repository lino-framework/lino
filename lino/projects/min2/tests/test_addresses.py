# -*- coding: utf-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Test certain aspects of `lino.modlib.addresses`.

This module is part of the Lino test suite. You can test only this
module by issuing either::

  $ go min2
  $ python manage.py test tests.test_addresses

or::

  $ go lino
  $ python setup.py test -s tests.ProjectsTests.test_min2


"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from lino.core.gfks import gfk2lookup
from lino.api import rt

from lino.modlib.gfks.mixins import Controllable

from lino.utils.djangotest import RemoteAuthTestCase

from lino.core.utils import full_model_name


def create(m, **kw):
    obj = m(**kw)
    obj.full_clean()
    obj.save()
    obj.after_ui_save(None, None)
    return obj


class QuickTest(RemoteAuthTestCase):

    fixtures = ['std', 'demo_users', 'few_countries', 'few_cities']

    def test_this(self):

        Company = rt.modules.contacts.Company
        Address = rt.modules.addresses.Address
        Place = rt.modules.countries.Place
        Problem = rt.modules.plausibility.Problem
        eupen = Place.objects.get(name="Eupen")
        ar = rt.modules.contacts.Companies.request()
        self.assertEqual(Address.ADDRESS_FIELDS, set([
            'city', 'street_box', 'region', 'street_no',
            'street', 'addr2', 'addr1', 'country', 'zip_code']))
        
        def assert_check(obj, expected):
            qs = Problem.objects.filter(**gfk2lookup(Problem.owner, obj))
            got = '\n'.join([p.message for p in qs])
            self.assertEqual(got, expected)

        obj = create(Company, name="Owner with empty address")
        obj.check_plausibility(ar, fix=False)
        assert_check(obj, '')
        obj.delete()

        self.assertEqual(Company.objects.count(), 0)
        self.assertEqual(Address.objects.count(), 0)

        doe = create(Company, name="Owner with address", city=eupen)

        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 0)

        assert_check(doe, '')  # No problems yet since not checked
        doe.check_plausibility(ar, fix=False)
        assert_check(
            doe, '(\u2605) Owner with address, but no address record.')

        addr = doe.get_primary_address()
        self.assertEqual(addr, None)

        doe.check_plausibility(ar, fix=True)
        assert_check(doe, '')  # problem has been fixed
        addr = doe.get_primary_address()
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(addr.city, eupen)
        self.assertEqual(addr.primary, True)

        addr.primary = False
        addr.save()
        addr = doe.get_primary_address()
        self.assertEqual(addr, None)
        self.assertEqual(Address.objects.count(), 1)

        doe.check_plausibility(ar, fix=False)
        assert_check(doe, '(\u2605) Unique address is not marked primary.')

        Address.objects.all().delete()
        self.assertEqual(Address.objects.count(), 0)
        addr = doe.get_primary_address()
        self.assertEqual(addr, None)

        doe.check_plausibility(ar, fix=False)
        assert_check(
            doe, '(\u2605) Owner with address, but no address record.')

        doe.check_plausibility(ar, fix=True)
        assert_check(doe, '')  # problem has been fixed

        # next problem : owner differs from primary address
        doe.city = None
        doe.zip_code = ''
        doe.full_clean()
        self.assertEqual(doe.city, None)
        doe.save()
        doe.check_plausibility(ar, fix=False)
        self.assertEqual(Address.objects.count(), 1)
        assert_check(
            doe, "Primary address differs from owner address "
            "(city:Eupen->None, zip_code:4700->).")
        # Lino does repair this automatically since we don't know
        # which data is correct.
        doe.check_plausibility(ar, fix=True)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(doe.city, None)
        addr = doe.get_primary_address()
        self.assertEqual(addr.city, eupen)
        self.assertEqual(addr.primary, True)
        
        # next problem: multiple primary address.
        # recover from previous test.
        doe.city = eupen
        doe.full_clean()
        doe.save()
        self.assertEqual(doe.city, eupen)
        self.assertEqual(doe.zip_code, '4700')
        addr = doe.get_primary_address()
        addr.id = None
        addr.save()
        self.assertEqual(Address.objects.count(), 2)
        doe.check_plausibility(ar, fix=False)
        assert_check(doe, "Multiple primary addresses.")
