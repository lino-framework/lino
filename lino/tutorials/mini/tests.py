# -*- coding: utf-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This module contains some quick tests:

- In a :class:`lino.modlib.sepa.models.Account`:

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

from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase


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
                {'bic': ['BIC codes have either 8 or 11 characters.']})

        # Raise ValidationError when no BIC is given
        obj = sepa.Account(partner=partner)
        try:
            obj.full_clean()
            self.fail("Expected ValidationError")
        except ValidationError as e:
            self.assertEqual(
                e.message_dict,
                {'iban': [u'This field cannot be blank.']})
