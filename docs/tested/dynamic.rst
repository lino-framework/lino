.. _lino.tested.dynamic:

==============
Dynamic models
==============

.. to run only this test:
  $ python setup.py test -s tests.DocsTests.test_dynamic

This document collects ideas on one possible way for working around
`inject_field` (:ticket:`246`)

General stuff:

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.min2.settings.doctests'
>>> from lino.api.doctest import *


BTW: The `dynamic-models
<http://dynamic-models.readthedocs.org/en/latest/>`_ project confirms
that it is possible.


First
=====

We will add a new attribute :attr:`dynamic_models
<lino.core.plugin.Plugin.dynamic_models>` for
:class:`lino.core.plugin.Plugin`.  This is a list or tuple of strings,
each string is of the form ``"<app_label>.<ModelName>"`` and specifies
a model whose class object should get *dynamically factored*.

When the Site object instantiates (i.e. before Django sees the
settings) it will collect the `dynamic_models` of all plugins and
create dynamic class objects for each of them. These class objects
inherit from all mixins found in all installed plugins.

With at least one gotcha: these mixins must get defined in a module
called :xfile:`bases.py`. That's because we cannot import any
:xfile:`models.py` file before 

Models that are candidates for dynamic factoring must use the
`is_abstract_model <lino.core.site.Site.is_abstract_model>` method
when declaring their inner `Meta` class.  But then?


Second
======

:xfile:`system/__init__.py`::

    class Plugin(ad.Plugin):
        ...

:xfile:`system/mixins.py`::

    class SiteConfigBase(dd.Model):

        class Meta:
            abstract = True
            verbose_name = _("Site configuration")
    
:xfile:`system/models.py`::

    from .mixins import *

    SiteConfig = dd.dynamic_model(SiteConfigBase)



:xfile:`other/__init__.py`::

    class Plugin(ad.Plugin):
        ...

:xfile:`other/mixins.py`::

    from lino.modlib.system.mixins import SiteConfigBase

    class OtherSiteConfig(SiteConfigBase):

        class Meta:
            abstract = True
    
:xfile:`other/models.py`::

    from .mixins import *


But how to implement `dd.dynamic_model(SiteConfigBase)`? The challenge
is that Lino must discover all abstract models which inherit from the
given class.

Abstract models are not stored in the models cache:

>>> from lino import AFTER17
>>> if AFTER17:
...     from django.apps import apps
...     [m for m in apps.get_models() if m._meta.abstract]
... else:
...     from django.db import models
...     [m for m in models.get_models(only_installed=False) if m._meta.abstract]
[]

And anyway the models cache is ready only when all models modules have
been imported. Which means that it is not easy.
