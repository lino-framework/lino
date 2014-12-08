# -*- coding: utf-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""This module contains "quick" tests that are run on a demo database
without any fixture. You can run only these tests by issuing either::

  $ go min2
  $ python manage.py test

or::

  $ go lino
  $ python setup.py test -s tests.ProjectsTests.test_min2

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from lino import rt

from lino.modlib.contenttypes.mixins import Controllable

from lino.utils.djangotest import RemoteAuthTestCase

from lino.core.dbutils import full_model_name


class QuickTest(RemoteAuthTestCase):

    fixtures = ['std', 'few_countries']

    def test00(self):
        self.assertEqual(1 + 1, 2)

    def test_controllables(self):
        # When I delete a database object, Lino also deletes those
        # objects who are related through a GenericForeignKey
        found = []
        for M in rt.models_by_base(Controllable):
            found.append(full_model_name(M))
        expected = """excerpts.Excerpt outbox.Mail outbox.Attachment
        notes.Note uploads.Upload cal.Task cal.Event""".split()
        self.assertEqual(found, expected)

        Person = rt.modules.contacts.Person
        Note = rt.modules.notes.Note
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(Note.objects.count(), 0)

        def create(m, **kw):
            obj = m(**kw)
            obj.full_clean()
            obj.save()
            return obj

        doe = create(Person, first_name="John", last_name="Doe")
        note = create(Note, owner=doe, body="John Doe is a fink!")

#         ses = rt.login()
#         s = rt.modules.notes.Notes.to_rst(ar, column_names="id owner")
#         # s = ses.show('notes.Notes', column_names="id owner")
#         self.assertEqual(s, """\
# ==== ===============
#  ID   Controlled by
# ---- ---------------
#  1    **John Doe**
# ==== ===============
# """)

        self.assertEqual(note.disable_delete(), None)
        self.assertEqual(Note.allow_cascaded_delete, [])
        self.assertEqual(
            doe.disable_delete(),
            "Cannot delete John Doe because 1 Notes refer to it.")

