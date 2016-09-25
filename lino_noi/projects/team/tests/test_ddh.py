# -*- coding: utf-8 -*-
# Copyright 2016 Luc Saffre
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.

"""Runs some tests about the disable-delete handler and cascading deletes.

You can run only these tests by issuing::

  $ go noi
  $ cd lino_noi/projects/team
  $ python manage.py test tests.test_ddh

Or::

  $ go noi
  $ python setup.py test -s tests.DemoTests.test_std

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase
from lino.api import rt


def create(m, **kwargs):
    obj = m(**kwargs)
    obj.full_clean()
    obj.save()
    return obj
    

class DDHTests(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        from lino.modlib.users.choicelists import UserProfiles
        Ticket = rt.modules.tickets.Ticket
        # Session = rt.modules.clocking.Session
        User = rt.modules.users.User
        Star = rt.modules.stars.Star
        ContentType = rt.modules.contenttypes.ContentType
        ct_Ticket = ContentType.objects.get_for_model(Ticket)

        robin = create(User, username='robin',
                       profile=UserProfiles.admin,
                       language="en")

        def createit():
            return create(Ticket, summary="Test", reporter=robin)

        #
        # If there are no vetos, user can ask to delete it
        #
        obj = createit()
        obj.delete()

        obj = createit()

        if False:
            try:
                robin.delete()
                self.fail("Expected veto")
            except Warning as e:
                self.assertEqual(
                    str(e), "Cannot delete User robin "
                    "because 1 Tickets refer to it.")

        
        create(Star, owner=obj, user=robin)
        
        try:
            robin.delete()
            self.fail("Expected veto")
        except Warning as e:
            self.assertEqual(
                str(e), "Cannot delete User robin "
                "because 1 Stars refer to it.")

        self.assertEqual(Star.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

        try:
            obj.delete()
            self.fail("Expected veto")
        except Warning as e:
            self.assertEqual(
                str(e), "Cannot delete Ticket #2 (Test) because "
                "1 Stars refer to it.")
