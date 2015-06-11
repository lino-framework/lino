=========================
An introduction to Tables
=========================


Models, tables and views
========================

In a Lino application you don't write only *models* but also *tables*.
This tutorial explains what they are.

While your **models** describe how data is to be structured when
stored in the database, **tables** describe how data is to be
presented to users in tabular form.

Roughly speaking, Lino's "tables" are the equivalent of what Django
calls "views". With Lino you don't need to write views because Lino
writes them for you. (To be complete, tables correspond only to one
class of Django's views, sometimes referred to as "tabular" or "list"
views. The other class of views are "detail" views, for which you are
going to define *Layouts*, but we'll talk about these later.)

Don't get troubled by the fact that Django's models are called
"tables" by most database management systems.


An example
==========

Here is the :xfile:`models.py` file which we will use in this
tutorial:

.. literalinclude:: models.py

Here is the data we use to fill our database:

.. literalinclude:: fixtures/demo.py
  
.. 
    >>> from __future__ import print_function
    >>> from lino.utils.dpy import load_fixture_from_module

We will now initialize our database with this fixture::

  $ python manage.py initdb_demo

.. 
    >>> import tables.fixtures.demo as m
    >>> load_fixture_from_module(m)


Designing your tables
=====================

You will have noticed the last line of our :xfile:`models.py` file above::

  from .ui import *

The :xfile:`ui.py` file describes the tables we are going to use in
this tutorial:

.. literalinclude:: ui.py

Please note:

- Database *models* are usually named in *singular* form, tables in
  *plural* form.

- Tables may inherit from other tables (e.g. ``BooksByAuthor``)

- You may define your tables together with the models in your
  :file:`models.py` file, or in a separate file :file:`ui.py`. It's
  a matter of taste.  But if you separate them, then you must import
  that file from within your :file:`models.py` file so that they get
  discovered at startup.


What is a table?
================

A table, in general, is a rectangular thing divided into rows and
columns, used to display data.

For example, here is the "Authors" table of our database:

============ =========== =========
 First name   Last name   Country
------------ ----------- ---------
 Douglas      Adams       UK
 Albert       Camus       FR
 Hannes       Huttner     DE
============ =========== =========

A table is always about a given **database model**. The :attr:`model
<lino.core.dbtables.Table.model>` attribute of a Table is mandatory.
For every database model there should be at least one table. Lino will
generate a default table for models for which there is no table at
all.  Note that there may be *more than one table* for a given model.

The **columns** of a table correspond to the *fields* of your database
model. Every column has a **header** which is the `verbose_name` of
that field. The values in a column are of same **data type** for each
row. So Lino knows all these things. Only one information is missing:
the :attr:`column_names <lino.core.tables.AbstractTable.column_names>`
attribute defines *which* columns are to be listed, and in which
order. It is a simple string with a space-separated list of field
names.

The **rows** of a table can be **sorted** and **filtered**. These are
things which are done in Django on a QuerySet.  Lino doesn't reinvent
the wheel here and just forwards them to their corresponding Django
methods: :attr:`order_by <lino.core.tables.AbstractTable.order_by>`,
:attr:`filter <lino.core.tables.AbstractTable.filter>` and
:attr:`exclude <lino.core.tables.AbstractTable.exclude>`.

Tables can hold information which goes beyond a model or a
queryset. For example we set :attr:`hide_sums
<lino.core.tables.AbstractTable.hide_sums>` to `True` on the ``Books``
table because otherwise Lino would display a sum for the "published"
column.


Using tables without a web server
=================================

An important thing with tables is that they are independent of any
user interface. You define them once, and you can use them on the
console, in a script, in a unit test, in a web interface or in a GUI
window.

At this point of our tutorial, we cannot yet fire up a web browser
(because we need to explain a few more concepts like menus and layouts
before we can do that), but we can already play with our data using
Django's console shell::

  $ python manage.py shell

And please note that the following code snippets are tested as part of
Lino's test suite. Writing test cases is an important part of software
development. Writing test cases might look less funny than developing
cool widgets, but actually these are part of analyzing and describing
how your users want their data to be structured.  Which is the more
important part of software development.

So here is, again our ``Authors`` table, this time in a testable
console format:

>>> from lino.api.shell import *
>>> rt.show(tables.Authors)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
============ =========== =========
 First name   Last name   Country
------------ ----------- ---------
 Douglas      Adams       UK
 Albert       Camus       FR
 Hannes       Huttner     DE
============ =========== =========
<BLANKLINE>

And here is the ``Books`` table:

>>> rt.show(tables.Books)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
================= ====================================== ===========
 author            Title                                  Published
----------------- -------------------------------------- -----------
 Adams, Douglas    Last chance to see...                  1990
 Adams, Douglas    The Hitchhiker's Guide to the Galaxy   1978
 Huttner, Hannes   Das Blaue vom Himmel                   1975
 Camus, Albert     L'etranger                             1957
================= ====================================== ===========
<BLANKLINE>

These were so-called **master tables**.  We also have a slave table:

>>> adams = tables.Author.objects.get(last_name="Adams")
>>> rt.show(tables.BooksByAuthor, adams)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
=========== ======================================
 Published   Title
----------- --------------------------------------
 1978        The Hitchhiker's Guide to the Galaxy
 1990        Last chance to see...
=========== ======================================
<BLANKLINE>


Summary
=======

Tables are Python class objects which describe tabular data views in
an abstract way, i.e. independently of the user interface.
