.. _lino.tested.diamond:

===================
Diamond inheritance
===================

This document shows that Django ticket :djangoticket:`10808` exists in
Django 1.6 and has been solved in Django 1.7 (at least for some cases;
see :doc:`../diamond2/index` for a more complex case which is still
broken.)


.. This document is part of the test suite.  
   To test only this  document, run:

    $ python setup.py test -s tests.DocsTests.test_diamond

    doctest init:

    >>> from __future__ import print_function
    >>> #from lino.api.doctest import *

Here is our database structure:

.. literalinclude:: main/models.py

.. include:: django16.rst

.. include:: django17.rst



.. toctree::
    :hidden:
    
    django16
    django17
