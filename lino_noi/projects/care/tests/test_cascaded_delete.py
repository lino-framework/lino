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
  $ cd lino_noi/projects/care
  $ python manage.py test tests.test_cascaded_delete

Or::

  $ go noi
  $ python setup.py test -s tests.DemoTests.test_care

This tests for :ticket:`1177`, :ticket:`1180`, :ticket:`1181`

"""

from __future__ import unicode_literals
from __future__ import print_function
import six

from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase
from lino.api import rt


def create(m, **kwargs):
    obj = m(**kwargs)
    obj.full_clean()
    obj.save()
    return obj
    

class Tests(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        from lino.modlib.users.choicelists import UserProfiles
        User = rt.modules.users.User
        Faculty = rt.models.faculties.Faculty
        Competence = rt.models.faculties.Competence
        Ticket = rt.models.tickets.Ticket
        TicketStates = rt.actors.tickets.TicketStates

        general = create(Faculty, name="General work")
        special = create(Faculty, name="Special work", parent=general)

        alex = create(User, username='alex',
                       profile=UserProfiles.user,
                       language="en")
        
        bruno = create(User, username='bruno',
                       profile=UserProfiles.user,
                       language="en")
        
        berta = create(User, username='berta',
                       profile=UserProfiles.user,
                       language="en")
        
        create(Competence, user=bruno, faculty=special)
        create(Competence, user=alex, faculty=general)
        
        ticket1 = create(
            Ticket, summary="Need general help",
            reporter=berta, faculty=general)

        ticket2 = create(
            Ticket, summary="Need special help",
            reporter=berta, faculty=special)

        self.assertEqual(ticket1.state, TicketStates.todo)

        ar = rt.actors.faculties.AssignableWorkersByTicket.request(ticket1)
        s = ar.to_rst()
        # print(s)
        self.assertEquivalent("""
==============
 Benutzername
--------------
 alex
==============""", s)


        ar = rt.actors.faculties.AssignableWorkersByTicket.request(ticket2)
        s = ar.to_rst()
        # print(s)
        self.assertEquivalent("""
==============
 Benutzername
--------------
 alex
 bruno
==============""", s)


        # cannot delete a faculty when there are competences referring
        # to it:
        try:
            special.delete()
            self.fail("Expected veto")
        except Warning as e:
            self.assertEqual(
                six.text_type(e), "Kann Fähigkeit Special work nicht "
                "löschen weil 1 Kompetenzen darauf verweisen.")

        # you cannot delete a faculty when it is the parent of other
        # faculties
        try:
            general.delete()
            self.fail("Expected veto")
        except Warning as e:
            self.assertEqual(
                six.text_type(e), "Kann Fähigkeit General work nicht "
                "löschen weil 1 Kompetenzen darauf verweisen.")
            
        # deleting a user will automatically delete all their
        # competences:
        
        bruno.delete()
        alex.delete()

        self.assertEqual(Ticket.objects.count(), 2)

        # from lino.core.merge import MergePlan
        # mp = MergePlan(berta, None)
        # mp.analyze()
        # s = mp.logmsg()
        # print(s)
        # self.assertEqual(s, '')
        
        # Deleting a user who reported a ticket is not refused because
        # Ticket.reporter is nullable. The tickets won't be deleted,
        # but their `reporter` field will be set to NULL:

        if False:
        
            berta.delete()

            self.assertEqual(Ticket.objects.count(), 2)

            # ticket1 = Ticket.objects.get(pk=1)
            # ticket2 = Ticket.objects.get(pk=2)

            self.assertEqual(ticket1.reporter, None)
            self.assertEqual(ticket2.reporter, None)

        # make sure that database state is as expected:

        self.assertEqual(Faculty.objects.count(), 2)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 2)
        self.assertEqual(Competence.objects.count(), 0)
        
        
