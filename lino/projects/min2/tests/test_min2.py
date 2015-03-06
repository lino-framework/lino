# -*- coding: utf-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Test some things which happen when a database object is deleted.

This module is part of the Lino test suite. You can test only this
module by issuing either::

  $ go min2
  $ python manage.py test
  $ python manage.py test tests.test_min2.QuickTest.test_dupable

or::

  $ go lino
  $ python setup.py test -s tests.ProjectsTests.test_min2


When I delete a database object, Lino also deletes those objects who
are related through a GenericForeignKey.

For example excerpts (`excerpts.Excerpt`) are related to their
"controller" or "owner" via a *generic* foreign key (as every
Controllable).  What happens to an excerpt when you delete its owner?
The default behaviour is to delete them silently (cascaded delete).

Another example are notes (`notes.Note`) who are also Controllable.
But unlike excerpts, we don't want them to vanish when we delete their
owner. We want Lino to tell us "Cannot delete this record because
other database objects are referring to it".

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from lino import rt

from lino.modlib.contenttypes.mixins import Controllable

from lino.utils.djangotest import RemoteAuthTestCase

from lino.core.utils import full_model_name

def create(m, **kw):
    obj = m(**kw)
    obj.full_clean()
    obj.save()
    return obj


class QuickTest(RemoteAuthTestCase):

    fixtures = ['std', 'few_countries']

    def test_controllables(self):
        found = []
        for M in rt.models_by_base(Controllable):
            found.append(full_model_name(M))
        expected = """excerpts.Excerpt outbox.Mail outbox.Attachment
        notes.Note uploads.Upload cal.Task cal.Event""".split()
        self.assertEqual(found, expected)

        Person = rt.modules.contacts.Person
        Note = rt.modules.notes.Note
        Excerpt = rt.modules.excerpts.Excerpt
        ExcerptType = rt.modules.excerpts.ExcerptType
        ContentType = rt.modules.contenttypes.ContentType
        self.assertEqual(len(Person.allow_cascaded_delete), 0)
        self.assertEqual(len(Note.allow_cascaded_delete), 0)
        self.assertEqual(len(Excerpt.allow_cascaded_delete), 1)

        doe = create(Person, first_name="John", last_name="Doe")
        note = create(Note, owner=doe, body="John Doe is a fink!")
        ct = ContentType.objects.get_for_model(Note)
        etype = create(ExcerptType, name="Note", content_type=ct)
        excerpt = create(Excerpt, owner=note,
                         excerpt_type=etype)

        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Excerpt.objects.count(), 1)

        ar = rt.modules.notes.Notes.request()
        s = ar.to_rst(column_names="id owner")
        self.assertEqual(s, """\
==== ===============
 ID   Controlled by
---- ---------------
 1    **John Doe**
==== ===============
""")

        ar = rt.modules.excerpts.Excerpts.request()
        s = ar.to_rst(column_names="id owner")
        self.assertEqual(s, """\
==== ===============
 ID   Controlled by
---- ---------------
 1    **Note #1**
==== ===============
""")

        self.assertEqual(excerpt.disable_delete(), None)
        self.assertEqual(note.disable_delete(), None)
        self.assertEqual(doe.disable_delete(), None)
        # it is not "Cannot delete John Doe because 1 Notes refer to
        # it." because Note.owner is nullable.

        note.delete()
        self.assertEqual(Excerpt.objects.count(), 0)
        self.assertEqual(ExcerptType.objects.count(), 1)

    def test_dupable(self):
        
        Person = rt.modules.contacts.Person
        PhoneticWord = rt.modules.dedupe.PhoneticWord
        bernard = create(Person, first_name="Bernard", last_name="Bodard")
        
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(bernard.phonetic_words.count(), 2)
        self.assertEqual(PhoneticWord.objects.count(), 2)

        bernard2 = create(Person, first_name="Bernhard", last_name="Bodard")
        ar = rt.modules.dedupe.SimilarPartners.request(bernard2)
        self.assertEqual(ar.get_total_count(), 1)

