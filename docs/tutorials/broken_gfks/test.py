# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.utils.test import DocTest
from lino.utils.djangotest import WebIndexTestCase

from django.conf import settings

from lino.api import rt
from lino.utils.djangotest import TestCase


class TestCase(TestCase):

    def test01(self):
        """We create a member, and a Note and a Memo whose `owner` fields
        point to that member. And then we delete that member.

        """

        Member = rt.modules.broken_gfks.Member
        Note = rt.modules.broken_gfks.Note
        Memo = rt.modules.broken_gfks.Memo
        BrokenGFKs = rt.modules.contenttypes.BrokenGFKs

        gfklist = [
            (f.model, f.fk_field, f.ct_field)
            for f in settings.SITE.kernel.GFK_LIST]
        self.assertEqual(gfklist, [
            (Note, 'owner_id', 'owner_type'),
            (Memo, 'owner_id', 'owner_type')])

        def create_objects():
            mbr = Member(name="John")
            mbr.save()

            self.assertEqual(mbr.name, "John")
            Note(owner=mbr, subject="test").save()
            Memo(owner=mbr, subject="test").save()
            return mbr

        mbr = create_objects()
        self.assertEqual(Member.objects.all().count(), 1)
        self.assertEqual(Note.objects.all().count(), 1)
        self.assertEqual(Memo.objects.all().count(), 1)
        # Django does not prevent us from deleting the member, and it
        # will leave the note and the memo in the database.
        mbr.delete()
        self.assertEqual(Member.objects.all().count(), 0)
        self.assertEqual(Note.objects.all().count(), 1)
        self.assertEqual(Memo.objects.all().count(), 1)

        ar = BrokenGFKs.request()
        rst = BrokenGFKs.to_rst(ar)
        # print rst
        self.assertEqual(rst, """\
================ ================= ============================================================
 Database model   Database object   Message
---------------- ----------------- ------------------------------------------------------------
 **note**         **Note object**   Invalid primary key 1 for broken_gfks.Member in `owner_id`
 **memo**         **Memo object**   Invalid primary key 1 for broken_gfks.Member in `owner_id`
================ ================= ============================================================
""")

