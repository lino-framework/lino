.. _dev.testing:

=========================
Testing Lino applications
=========================

You can write test suites for a Lino application like for any other
Django project.

Lino adds to Django a set of tools, conventions, ideas and suggestions 
for testing your applications.

Demo databases.

Lino adds a new style of test cases: 
test cases that use a `django.test.Client`,
but *on the project demo database* 
and *not* on a test database as the Django test runner creates it.

The advantage is that they access the existing demo database and thus
don't need to populate it (load the demo fixtures) for each test run.

A limitation of these cases is of course that they may not modify the
database.

All these would deserve a whole chapter of documentation.  I'll do my
best to fill up this hole...  meanwhile you must use the source, Luke!

.. toctree::

    tested_docs


- Extended TestCase classes:

  - :mod:`atelier.test`
  - :mod:`lino.utils.pythontest` and :mod:`lino.utils.djangotest`
  - :mod:`lino.utils.test`
