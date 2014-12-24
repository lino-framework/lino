===========================
Application Design (``ad``) 
===========================

.. This is part of the Lino test suite. To test only this document:

  $ python setup.py test -s tests.DocsTests.test_ad

.. module:: ad

The :mod:`lino.ad` module is a shortcut to those parts of Lino which
are used in your :xfile:`settings.py` files and in the
:xfile:`__init__.py` files of your apps.  The name ``ad`` stands for
"Application Design".  Application design happens **during** the
import of your Django **settings** and **before** your **models** get
imported.

Lino defines two classes 
:class:`Site <lino.core.site_def.Site>` and
:class:`Plugin <lino.core.plugin.Plugin>` which are heavily used to do lots of
magic and to make apps more pleasant to configure.

.. contents:: 
   :local:
   :depth: 2


.. note:: 

  This is a tested document. You can test it using::

    $ python setup.py test -s tests.DocsTests.test_site

.. 
  >>> import os
  >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
  ...   'lino.projects.docs.settings.demo'
  >>> from lino.runtime import *


  

