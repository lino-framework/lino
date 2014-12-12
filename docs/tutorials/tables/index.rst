=========================
An introduction to Tables
=========================

In a Lino application, you don't only write *models* but also
*tables*.

**Models** describe how data is to be structured when stored in the
database.
**Tables** describe how this data is to be presented to users in
 tabular form.


Please have a look at the :xfile:`models.py` file which we will use in
this tutorial:

.. literalinclude:: models.py

- For every model (conventionally a word in singular form) we have at
  least one table (conventionally a word in plural form).
- There may be more than one table for a given model
- Tables may inherit from other tables (e.g. `BooksByAuthor`)
- We suggest to write your table definitions in the same file as their
  models. But that's a matter of taste.

Here is a :ref:`fixture <dpy>` we use to fill some demo data:

.. literalinclude:: fixtures/demo.py
  
.. 
    >>> from __future__ import print_function
    >>> from lino.runtime import *
    >>> globals().update(tables.__dict__)
    >>> from lino.utils.dpy import load_fixture_from_module

We will now initialize our database with this fixture::

  $ python manage.py initdb_demo

.. 
    >>> import tables.fixtures.demo as m
    >>> load_fixture_from_module(m)
    
At this point, we cannot yet fire up a web browser (we need to explain
a few more concepts like menus and layouts before we can do that), but
we can already play with our data using Django's console shell::

  $ python manage.py shell

>>> rt.show(Authors)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
============ =========== =========
 First name   Last name   Country
------------ ----------- ---------
 Douglas      Adams       UK
 Albert       Camus       FR
 Hannes       Huttner     DE
============ =========== =========
<BLANKLINE>


>>> rt.show(Books)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
==================== ====================================== ===========
 author               Title                                  Published
-------------------- -------------------------------------- -----------
 Adams, Douglas       Last chance to see...                  1990
 Adams, Douglas       The Hitchhiker's Guide to the Galaxy   1978
 Huttner, Hannes      Das Blaue vom Himmel                   1975
 Camus, Albert        L'etranger                             1957
 **Total (4 rows)**                                          **7900**
==================== ====================================== ===========
<BLANKLINE>


>>> adams = Author.objects.get(last_name="Adams")
>>> rt.show(BooksByAuthor, adams)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
=========== ======================================
 Published   Title
----------- --------------------------------------
 1978        The Hitchhiker's Guide to the Galaxy
 1990        Last chance to see...
 **3968**
=========== ======================================
<BLANKLINE>


The important point of these examples is that tables are Python
classes which describe tabular data views in an abstract way,
i.e. independently of the user interface.
