.. _settings:

=============================
Lino and your Django settings
=============================

.. envvar:: DJANGO_SETTINGS_MODULE
  
The **Django settings module** is the most important thing in Django.
Almost everything you do with Django requires the settings module to
be loaded. Django does that automatically, and it (usually) reads the
:envvar:`DJANGO_SETTINGS_MODULE` environment variable which is
expected to contain the **Python name** of an importable module.

.. xfile:: settings.py

The actual filename of a Django settings module is not important, but
by convention it is often in a file named :xfile:`settings.py`.
That's why we sometimes speak about "the :xfile:`settings.py` file"
when actually we mean the Django settings module.

Django's `startproject` command generates a :xfile:`settings.py` file
which contains already 82 lines of text (Django version 1.6.9).  

Lino helps you to keep :xfile:`settings.py` files small because it
delegates the responsibility of maintaining default values for Django
settings to the application developer.

The typical local :xfile:`settings.py` file for a Lino project
consists of two lines (plus, on a production site, the lines for
defining your :setting:`DATABASES` setting).

This is possible because Lino adds one rather special setting called
:setting:`SITE`.

.. setting:: SITE

Lino expects one important variable in your :xfile:`settings.py` file.
It must be named :setting:`SITE`, and it must contain an instance of
the :class:`lino.core.site.Site` class.


Basics
======


Here is a typical :xfile:`settings.py` file of a Lino project::

  from ... import *
  SITE = Site(globals())
  # ... your local settings here

That is, you import the :class:`lino.core.site.Site` class (or --more
often-- some subclass thereof), then assign an instance of it to a
variable whose name must be ``SITE``.

Unlike most other Django settings, ``SITE`` contains a **Python
object** which has methods that can be called by application code at
runtime.

When instantiating a :class:`Site <lino.core.site.Site>` in a
:xfile:`settings.py` file, the first parameter must be ``globals()``,
because Lino is going to automatically set certain Django
settings. For example :setting:`INSTALLED_APPS` and
:setting:`DATABASES`.

A complete list is in :doc:`/ref/settings`.

If you want to modify one of these settings, do it *after*
instantiating your :setting:`SITE`.

The optional second positional argument should be the value of your
original :setting:`INSTALLED_APPS` (to which Lino will automatically
add some).  If you don't specifiy this argument, then you should
specify your installed apps by overriding
:meth:`lino.core.site.Site.get_installed_apps`.

Besides this you can override any class argument using a keyword
argment of same name:

- :attr:`lino.core.site.Site.title`
- :attr:`lino.core.site.Site.verbose_name`

You've maybe heard that it is not allowed to modify Django's settings
once it has started.  But there's nothing illegal with this here
because this happens before Django has seen your :xfile:`settings.py`.

Lino does more than this. It will for example read the `__file__
<http://docs.python.org/2/reference/datamodel.html#index-49>`__
attribute of this, to know where your :file:`settings.py` is in the
file system.


.. _djangosite_local:

The ``djangosite_local.py`` file
================================

The :ref:`djangosite_local.py <djangosite_local>` file is another
technique which Lino adds to plain Django.

When a :class:`lino.core.site.Site` gets instantiated, it will try to
import an module named ``djangosite_local``, and if that module exists
and has a function named ``setup_site``, Lino will call this function.

This mechanism is used on servers where many Lino sites are running to
provide local server-wide default settings.
