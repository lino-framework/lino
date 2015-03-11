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

from lino.api import rt

from lino.modlib.contenttypes.mixins import Controllable

from lino.utils.djangotest import RemoteAuthTestCase

from lino.core.utils import full_model_name


def create(m, **kw):
    obj = m(**kw)
    obj.full_clean()
    obj.save()
    obj.after_ui_save(None, None)
    return obj


class QuickTest(RemoteAuthTestCase):

    fixtures = ['std', 'few_countries', 'few_cities']

    def test_this(self):

        Company = rt.modules.contacts.Company
        Address = rt.modules.addresses.Address
        Place = rt.modules.countries.Place
        eupen = Place.objects.get(name="Eupen")

        doe = create(Company, name="Example", city=eupen)

        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 0)

        addr = doe.get_primary_address()
        self.assertEqual(addr, None)

        addr = doe.get_primary_address(True)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(addr.city, eupen)
        self.assertEqual(addr.primary, True)

        addr.primary = False
        addr.save()
        addr = doe.get_primary_address()
        self.assertEqual(addr.city, eupen)
        self.assertEqual(addr.primary, False)
        self.assertEqual(Address.objects.count(), 1)

        addr.delete()
        self.assertEqual(Address.objects.count(), 0)
        addr = doe.get_primary_address()
        self.assertEqual(addr, None)
