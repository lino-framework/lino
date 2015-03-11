# -*- coding: utf-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino Welfare project.
# Lino Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino Welfare; if not, see <http://www.gnu.org/licenses/>.

"""This module contains some quick tests:

- In a :class:`ml.sepa.Account`:

  - Fill IBAN and BIC from Belgian NBAN or IBAN
  - Test whether the record is being validated.


You can run only these tests by issuing::

  $ cd lino/tutorials/mini
  $ python manage.py test

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

# from django.conf import settings
from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase

# from lino.api import dd, rt


class QuickTest(RemoteAuthTestCase):
    maxDiff = None

    def test_sepa(self):
        from lino.api.shell import sepa, contacts
        partner = contacts.Partner(name="Foo")
        partner.full_clean()
        partner.save()

        # Fill IBAN and BIC from Belgian NBAN
        obj = sepa.Account(partner=partner, iban="001-1148294-84")
        obj.full_clean()
        self.assertEqual(obj.bic, 'GEBABEBB')
        self.assertEqual(obj.iban, 'BE03001114829484')

        # Fill BIC from Belgian IBAN
        obj = sepa.Account(partner=partner, iban="BE03001114829484")
        obj.full_clean()
        self.assertEqual(obj.bic, 'GEBABEBB')
        self.assertEqual(obj.iban, 'BE03001114829484')

        # Raise ValidationError when invalid IBAN
        obj = sepa.Account(partner=partner, iban="BE03001114829483")
        try:
            obj.full_clean()
            self.fail("Expected ValidationError")
        except ValidationError as e:
            self.assertEqual(
                e.message_dict,
                {'iban': ['Not a valid IBAN.']})

        # Raise ValidationError when invalid BIC
        obj = sepa.Account(
            partner=partner, iban="BE03001114829484", bic="FOO")
        try:
            obj.full_clean()
            self.fail("Expected ValidationError")
        except ValidationError as e:
            self.assertEqual(
                e.message_dict,
                {'bic': ['A SWIFT-BIC is either 8 or 11 characters long.']})

        # Raise ValidationError when no BIC is given
        obj = sepa.Account(partner=partner)
        try:
            obj.full_clean()
            self.fail("Expected ValidationError")
        except ValidationError as e:
            self.assertEqual(
                e.message_dict,
                {'iban': [u'This field cannot be blank.']})
