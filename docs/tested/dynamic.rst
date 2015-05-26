.. _lino.tested.dynamic:

Dynamic models
==============

.. to run only this test:

  $ python setup.py test -s tests.DocsTests.test_dynamic

General stuff:

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.min2.settings.doctests'
>>> from lino.api.doctest import *

Abstract models are not stored in the models cache:

>>> from django.db import models
>>> [m for m in models.get_models(only_installed=False) if m._meta.abstract]
[]

Which means that it is not easy for Lino to discover all abstract
models which inherit from a given class.
