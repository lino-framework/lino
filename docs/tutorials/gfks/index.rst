.. _lino.tutorial.gfks:

=================================
A tested example of GFK fields
=================================

.. This document is part of the test suite.  To test only this
   document, run:

     $ python setup.py test -s tests.DocsTests.test_gfks

   Or:

     $ cd docs/tutorials/gfks
     $ python manage.py test


This tutorial project illustrates some aspects of :doc:`/dev/gfks`.

It also illustrates how tested documents (i.e. unit tests which use
Python's doctest module) and "normal" unittest modules can complement
each other.

The :xfile:`models.py` file defines four database models:

.. literalinclude:: models.py

A `Member` is the potential owner of the other three things.

A `Comment` has `allow_cascaded_delete` and thus will be silently deleted if the owner gets deleted.
A `Note` does not allow cascaded delete, and thus will cause a veto when we try to delete a member which is owner of some note.
A `Memo` has a nullable `owner` field and thus will be cleared when we delete the owner.


This project also uses :mod:`lino.modlib.contenttypes`. We define this
in our :xfile:`settings.py` file:

.. literalinclude:: settings.py

Doctests initialization:

>>> from __future__ import print_function, unicode_literals
>>> from lino.api.doctest import *
>>> Member = rt.modules.gfks.Member
>>> Comment = rt.modules.gfks.Comment
>>> Note = rt.modules.gfks.Note
>>> Memo = rt.modules.gfks.Memo

A utility function:

>>> def status():
...     return [m.objects.all().count() for m in Member, Comment, Note, Memo]
...         

We create a member and three GFK-related objects whose `owner` fields
point to that member. And then we try to delete that member.

>>> mbr = Member(name="John")
>>> mbr.save()
>>> Comment(owner=mbr, text="Just a comment").save()
>>> Note(owner=mbr, text="John owes us 100€").save()
>>> Memo(owner=mbr, text="About John and his friends").save()

>>> print status()
[1, 1, 1, 1]

The :meth:`disable_delete <lino.core.model.Model.disable_delete>`
method also sees these objects:

>>> print(unicode(mbr.disable_delete()))
Cannot delete John because 1 notes refer to it.

This means that Lino would prevent users from deleting this member
through the web interface.

Lino also protects normal application code from deleting a member:

>>> mbr.delete()
Traceback (most recent call last):
  ...
Warning: Cannot delete John because 1 notes refer to it.

All objects are still there:

>>> print status()
[1, 1, 1, 1]

Django does **not** prevent us from deleting the member, and it will
leave both the note and the memo in the database:

>>> from django.db import models
>>> models.Model.delete(mbr)
>>> print status()
[0, 1, 1, 1]


Users can see them by opening the :class:`BrokenGFKs
<lino.modlib.contenttypes.models.BrokenGFKs>` table:

>>> rt.show(contenttypes.BrokenGFKs)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
================ ==================== =====================================================
 Database model   Database object      Message
---------------- -------------------- -----------------------------------------------------
 **comment**      **Comment object**   Invalid primary key 1 for gfks.Member in `owner_id`
 **note**         **Note object**      Invalid primary key 1 for gfks.Member in `owner_id`
 **memo**         **Memo object**      Invalid primary key 1 for gfks.Member in `owner_id`
================ ==================== =====================================================
<BLANKLINE>


Tested twice
============

This tutorial project is tested twice.  Most things which we tested in
the present document are also being tested in a plain unittest module:

.. literalinclude:: test.py

