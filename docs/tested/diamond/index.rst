.. _lino.tested.diamond:

===================
Diamond inheritance
===================

This document shows that the problem described in Django ticket
:djangoticket:`10808` still exists in Django 1.6 and that it has been
solved in Django 1.7 at least for the described case (see
:doc:`../diamond2/index` for a more complex case).

The source code used to generate and test this document is at
:srcref:`docs/tested/diamond/`.


.. This document is part of the test suite.  
   To test only this  document, run:

    $ python setup.py test -s tests.DocsTests.test_diamond

    doctest init:

    >>> from __future__ import print_function
    >>> #from lino.api.doctest import *

Our database structure is defined in :file:`main/models.py` as
follows:

.. literalinclude:: main/models.py

.. include:: django16.rst

.. include:: django17.rst



.. toctree::
    :hidden:
    
    django16
    django17
