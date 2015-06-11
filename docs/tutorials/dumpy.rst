.. _lino.tutorial.dpy:

===============================
Introduction to Python fixtures
===============================

.. to run only this test:
  $ python setup.py test -s tests.DocsTests.test_dumpy

This tutorial shows how to use :doc:`the Python serializer
</topics/dpy>` for writing and loading demonstration data samples for
application prototypes and test suites.


You know that a *fixture* is a portion of data (a collection of data
records in one or several tables) which can be loaded into a database.
Read more about fixtures in the `Providing initial data for models
<https://docs.djangoproject.com/en/1.6/howto/initial-data/>`_ article
of the Django documentation.  This article says that "fixtures can be
written as XML, YAML, or JSON documents".  Well, Lino adds another
format to this list: Python.

Here is a fictive minimal example of a Python fixture::

  from myapp.models import Foo
  def objects():
      yield Foo(name="First")
      yield Foo(name="Second")

A Python fixture is a normal Python module, stored in a file ending
with `.py` and designed to being imported and exectued during Django's
`loaddata
<https://docs.djangoproject.com/en/1.6/ref/django-admin/#django-admin-loaddata>`_
command.

It is expected to contain a function named ``objects`` which must take
no parameters and which must return or yield a list of database
objects.


The :manage:`initdb` and :manage:`initdb_demo` commands
-------------------------------------------------------

Remember that we told you (in :ref:`lino.tutorial.hello`) 
to "prepare your database" by running the command::

  $ python manage.py initdb_demo
  
The :xfile:`manage.py` Python script is the standard Django interface
for running a so-called **administrative task** (if you did't know
that, please read `django-admin.py and manage.py
<https://docs.djangoproject.com/en/1.6/ref/django-admin/>`_).

The :manage:`initdb_demo` command which we used here is a `custom
django-admin command
<https://docs.djangoproject.com/en/1.6/howto/custom-management-commands/>`_
provided by Lino.  

It does nothing else than to call :manage:`initdb`
with the **demo fixtures**.

The **demo fixtures** is a predefined set of fixture names,
defined by the application developer in 
the :attr:`demo_fixtures <lino.core.site.Site.demo_fixtures>` setting.
The `min1` app has the following demo fixtures:

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino.projects.min1.settings.demo'
>>> from django.conf import settings
>>> settings.SITE.demo_fixtures
'std demo demo2'

So the ``initdb_demo`` command above is equivalent to::
  
  $ python manage.py initdb std demo demo2

The :manage:`initdb` command
----------------------------

The :manage:`initdb` command performs three actions in one:

- it flushes the database specified in your :xfile:`settings.py`,
  i.e. issues a ``DROP TABLE`` for every table used by your application.
 
- then runs Django's `syncdb` command to re-create all tables,

- and finally runs Django's `loaddata` command to load the specified
  fixtures.

So the above line is roughly equivalent to::

  $ python manage.py flush
  $ python manage.py syncdb
  $ python manage.py loaddata std demo demo2
  
Removing all tables may sound dangerous, but that's what we want when
we want to "just have a look at this application", or when we are
developing a prototype and just made some changes to the database
structure.  We assume that nobody will ever let a Lino application and
some other application share the same database.

Playing with fixtures
---------------------

Have a look at the following fixture files

- :srcref:`few_countries </lino/modlib/countries/fixtures/few_countries.py>`
  and :srcref:`all_countries </lino/modlib/countries/fixtures/all_countries.py>`

- :srcref:`few_languages </lino/modlib/countries/fixtures/few_languages.py>`
  and :srcref:`all_languages </lino/modlib/countries/fixtures/all_languages.py>`

- :srcref:`few_cities </lino/modlib/countries/fixtures/few_cities.py>`
  and :srcref:`be </lino/modlib/countries/fixtures/be.py>`.

Play with them::

  python manage.py initdb std all_countries be few_languages props demo 
  python manage.py initdb std few_languages few_countries few_cities demo 
  ...

Note that Python fixtures can also be used manually with
:manage:`loaddata`, in that case they behave like normal fixtures.

  python manage.py initdb
  python manage.py loaddata std
  python manage.py loaddata few_languages few_countries few_cities demo 
  ...



Writing your own fixture
------------------------

Create a directory named :xfile:`fixtures` in your local project
directory::

   mkdir ~/projects/mysite/fixtures
   
Create a file `dumpy1.py` in that directory as the following.
But put your real name and data, this is your local file.

.. literalinclude:: dumpy1.py
    :linenos:
    

Try to apply this fixture::    

  $ python manage.py initdb dumpy1
  Gonna flush your database (myproject).
  Are you sure (y/n) ?y
  INFO Lino initdb ('dumpy1',) started on database myproject.
  INFO Lino version 1.1.11 using Python 2.7.1, Django 1.4 pre-alpha SVN-16280, 
  python-dateutil 1.4.1, Cheetah 2.4.4, docutils 0.7, PyYaml 3.08, 
  pyratemp (not installed), xhtml2pdf 3.0.32, ReportLab Toolkit 2.4, 
  appy.pod 0.6.6 (2011/04/26 20:50)
  No fixtures found.
  INFO Saved 2 instances from t:\hgwork\lino\docs\tutorials\dumpy1.py.
  Installed 1 object(s) from 1 fixture(s)
  INFO Lino initdb done ('dumpy1',) on database t:\data\luc\lino\dsbe\dsbe_test.db.

A technical detail: you cannot use relative imports in a Python
fixture.  See `here
<http://stackoverflow.com/questions/4907054/loading-each-py-file-in-a-path-imp-load-module-complains-about-relative-impor>`__


.. _tutorial.instantiator:

Introducing the ``Instantiator`` class
--------------------------------------

Since `.py` fixtures are normal Python modules, there are no more
limits to our phantasy when creating new objects.  A first thing that
drops into mind is: there should be a more "compact" way to create
many records of a same table.

A quick generic method for for writing more compact fixtures this is
the :class:`lino.utils.instantiator.Instantiator` class.  Here is the
same fixture in a more compact wayusing an instantiator:

.. literalinclude:: dumpy2.py
    :linenos:


The :class:`lino.utils.instantiator.Instantiator` class just helps to
eliminate some lines of the code, nothing more (and nothing
less). Compare the two `demo.py` files on this page and imagine you
want to maintain these fixtures and ask: which one will be easier to
maintain. For example add a third user, or add a new field for every
user.

You can also use python fixtures to generate random and massive amount
of data. Look for example at the source code of
:mod:`lino.modlib.notes.fixtures.demo`.


Third step
----------

Play around and try to add some more objects to your local demo database!


The default demo fixtures
-------------------------

The :ref:`cosi` application developer had decided that a 
demo site should by default load just *this* set of fixtures.
How did he do that?
Look at the source code of  
:srcref:`/lino/projects/min1/settings/__init__.py`
where he overrides the 
:setting:`demo_fixtures` 
attribute of his :class:`Site` 
class, setting it to::

    demo_fixtures = 'std few_countries few_cities few_languages furniture demo demo2'.split()


Conclusion
----------

Python fixtures are an important tool for application developers
because 

- they are more flexible than json or xml fixtures and easy to adapt 
  when your database structure changes.
  
- they provide a simple interface to deploy demo data for an application


