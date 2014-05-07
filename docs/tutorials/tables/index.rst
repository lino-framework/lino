==============
Tables
==============

.. include:: /include/wip.rst

This is a tutorial to illustrate stuff explained in :ref:`dev.actors`.

Here is the :xfile:`models.py` file we will use for this tutorial:

.. literalinclude:: models.py

Here is the :ref:`fixture <dpy>` we use to fill some demo data:

.. literalinclude:: fixtures/demo.py
  
.. 
    >>> from __future__ import print_function
    >>> from lino import dd
    >>> from lino.runtime import *
    >>> globals().update(tables)
    >>> from north.dpy import load_fixture_from_module


>>> import tables.fixtures.demo as m
>>> load_fixture_from_module(m)

>>> dd.show(Authors)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
============ =========== =========
 First name   Last name   Country
------------ ----------- ---------
 Douglas      Adams       UK
 Albert       Camus       FR
 Hannes       Huttner     DE
============ =========== =========
<BLANKLINE>


>>> dd.show(Books)
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
>>> dd.show(BooksByAuthor, adams)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
=========== ======================================
 Published   Title
----------- --------------------------------------
 1978        The Hitchhiker's Guide to the Galaxy
 1990        Last chance to see...
 **3968**
=========== ======================================
<BLANKLINE>
