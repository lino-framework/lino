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

    fixtures = ['std', 'few_countries']

    def test_controllables(self):
        found = []
        for M in rt.models_by_base(Controllable):
            found.append(full_model_name(M))
        expected = """cal.Event cal.Task excerpts.Excerpt
        notes.Note notifier.Notification outbox.Attachment outbox.Mail
        plausibility.Problem uploads.Upload""".split()
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
 1    *John Doe*
==== ===============

""")

        ar = rt.modules.excerpts.Excerpts.request()
        s = ar.to_rst(column_names="id owner")
        self.assertEqual(s, """\
==== ===============
 ID   Controlled by
---- ---------------
 1    *Note #1*
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
        
        Company = rt.modules.contacts.Company
        Person = rt.modules.contacts.Person
        DupableWord = rt.modules.dupable_partners.Word

        bernard = create(Person, first_name="Bernard", last_name="Bodard")
        
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(bernard.dupable_words.count(), 2)
        self.assertEqual(DupableWord.objects.count(), 2)
        words = [o.word for o in DupableWord.objects.filter(owner=bernard)]
        self.assertEqual(words, [u'PTRT', u'PRNR'])

        bernard2 = create(Person, first_name="Bodard", last_name="Bernard")
        bernard3 = create(
            Person, first_name="Bernhard", last_name="Bodard")
        godard = create(Person, first_name="Bernard", last_name="Godard")
        erna = create(Person, first_name="Erna", last_name="Odar")
        bernard4 = create(
            Person, first_name="Bernard-Marie", last_name="Bodard")
        marie = create(Person, first_name="Marie", last_name="Bernard-Bodard")

        create(Company, name="Külamaja OÜ")

        def create_person(first, last):
            return create(Person, first_name=first, last_name=last)

        mm1 = create_person("Marie", "Meier")
        mm2 = create_person("Marie", "Meyer")

        def check(obj, expected):
            got = map(unicode, obj.find_similar_instances(4))
            got = '\n'.join(got)
            self.assertEqual(got, expected.strip())

        check(bernard, """
Bodard Bernard
Bernhard Bodard
Bernard-Marie Bodard
Marie Bernard-Bodard
""")

        check(bernard2, """
Bernard Bodard
Bernhard Bodard
Bernard-Marie Bodard
Marie Bernard-Bodard
""")

        check(bernard3, """
Bernard Bodard
Bodard Bernard
Bernard-Marie Bodard
Marie Bernard-Bodard
""")

        check(godard, "")
        check(erna, "")
        check(bernard4, """
Marie Bernard-Bodard""")
        check(marie, """
Bernard-Marie Bodard
Bernard Bodard
Bodard Bernard
Bernhard Bodard
""")

        check(mm1, "Marie Meyer")
        check(mm2, "Marie Meier")
