# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.utils.test import DocTest
from lino.utils.djangotest import WebIndexTestCase

from django.db import models
from django.conf import settings

from lino.api import rt
from lino.utils.djangotest import TestCase


class TestCase(TestCase):

    maxDiff = None

    def test01(self):
        """We create a member, and three GFK-related objects whose `owner`
        fields point to that member. And then we try to delete that
        member.

        """
        Member = rt.modules.gfktest.Member
        Note = rt.modules.gfktest.Note
        Memo = rt.modules.gfktest.Memo
        Comment = rt.modules.gfktest.Comment
        BrokenGFKs = rt.modules.gfks.BrokenGFKs

        def check_status(*args):
            for i, m in enumerate((Member, Comment, Note, Memo)):
                n = m.objects.all().count()
                if n != args[i]:
                    msg = "Expected %d objects in %s but found %d"
                    msg %= (args[i], m.__name__, n)
                    self.fail(msg)
        
        gfklist = [
            (f.model, f.fk_field, f.ct_field)
            for f in settings.SITE.kernel.GFK_LIST]
        self.assertEqual(gfklist, [
            (Comment, 'owner_id', 'owner_type'),
            (Note, 'owner_id', 'owner_type'),
            (Memo, 'owner_id', 'owner_type')])

        def create_objects():
            mbr = Member(name="John",id=1)
            mbr.save()

            self.assertEqual(mbr.name, "John")
            Comment(owner=mbr, text="Just a comment...").save()
            Note(owner=mbr, text="John owes us 100€").save()
            Memo(owner=mbr, text="More about John and his friends").save()
            return mbr

        mbr = create_objects()
        check_status(1, 1, 1, 1)
        try:
            mbr.delete()
        except Warning as e:
            self.assertEqual(
                unicode(e), "Cannot delete member John because 1 notes refer to it.")
        else:
            self.fail("Expected an exception")

        # they are all still there:
        check_status(1, 1, 1, 1)
        
        # delete the note manually
        Note.objects.all().delete()
        check_status(1, 1, 0, 1)
        mbr.delete()
        # the memo remains:
        check_status(0, 0, 0, 1)
        Memo.objects.all().delete()

        # The above behaviour is thanks to a `pre_delete_handler`
        # which Lino adds automatically. Theoretically it is no longer
        # possible to produce broken GFKs.  But now we disable this
        # `pre_delete_handler` and use Django's raw `delete` method in
        # order to produce some broken GFKs:

        from django.db.models.signals import pre_delete
        from lino.core.model import pre_delete_handler
        pre_delete.disconnect(pre_delete_handler)

        check_status(0, 0, 0, 0)
        mbr = create_objects()
        check_status(1, 1, 1, 1)
        models.Model.delete(mbr)

        pre_delete.connect(pre_delete_handler)

        # The member has been deleted, but all generic related objects
        # are still there:
        check_status(0, 1, 1, 1)

        # That's what the BrokenGFKs table is supposed to show:
        # rst = BrokenGFKs.request().table2rst()
        rst = BrokenGFKs.request().to_rst()
        # print rst
        self.assertEqual(rst, """\
================ ================== ======================================================== ========
 Database model   Database object    Message                                                  Action
---------------- ------------------ -------------------------------------------------------- --------
 *comment*        *Comment object*   Invalid primary key 1 for gfktest.Member in `owner_id`   delete
 *note*           *Note object*      Invalid primary key 1 for gfktest.Member in `owner_id`   manual
 *memo*           *Memo object*      Invalid primary key 1 for gfktest.Member in `owner_id`   clear
================ ================== ======================================================== ========

""")

