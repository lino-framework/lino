.. _lino.tutorial.broken_gfks:

=====================
Reporting broken GFKs
=====================

.. contents::
   :local:

The :xfile:`models.py` file:

.. literalinclude:: models.py

About this document
===================

This document is part of the Lino test suite. To test only this
document, run::

   $ python setup.py test -s tests.DocsTests.test_broken_gfks

This tutorial tests the same thing also as a unit test case:

.. literalinclude:: test.py

To run the test suite of this tutorial::

  $ cd docs/tutorials/broken_gfks
  $ python manage.py test

The above command will run the following code snippets in a subprocess
and check whether their output is the same as the one displayed here.

Doctests initialization:

>>> from __future__ import print_function
>>> from lino.api.doctest import *

>>> Member = rt.modules.broken_gfks.Member
>>> Note = rt.modules.broken_gfks.Note
>>> Memo = rt.modules.broken_gfks.Memo

We create a member:

>>> mbr = Member(name="John")
>>> mbr.save()
>>> Note(owner=mbr, subject="test").save()
>>> Memo(owner=mbr, subject="test").save()

>>> Member.objects.all().count()
1
>>> Note.objects.all().count()
1
>>> Memo.objects.all().count()
1

Django does not prevent us from deleting the member, and it will leave
the note in the database.

>>> mbr.delete()
>>> Member.objects.all().count()
0
>>> Note.objects.all().count()
1
>>> Memo.objects.all().count()
1


Show the list of broken GFKs:    

>>> rt.show(contenttypes.BrokenGFKs)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
================ ================= ============================================================
 Database model   Database object   Message
---------------- ----------------- ------------------------------------------------------------
 **note**         **Note object**   Invalid primary key 1 for broken_gfks.Member in `owner_id`
 **memo**         **Memo object**   Invalid primary key 1 for broken_gfks.Member in `owner_id`
================ ================= ============================================================
<BLANKLINE>

Here is our :xfile:`settings.py` file:

.. literalinclude:: settings.py

