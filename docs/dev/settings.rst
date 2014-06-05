.. _settings:

===================================
How Lino makes your Django settings
===================================


Basics
======

.. xfile:: settings.py

See :ref:`lino.tutorial.polls` 


To turn your Django project into a Lino site, you change your
:xfile:`settings.py` file as follows:

Before::

  # ... your settings 
  INSTALLED_APPS = ["myapp1", "myapp2"]
  # ... your settings 

After::

  from ... import Site
  SITE = Site(globals(), "myapp1", "myapp2")
  # ... your settings here

That is, you import the :class:`ad.Site` class (or -more often- some
subclass thereof), then assign an instance of it to a setting variable
whose name *must* be ``SITE``.

``SITE`` is the only name which Lino adds to Django's settings. Unlike
most other Django settings, ``SITE`` contains a **Python object**
which has methods that you can call at runtime.

When instantiating a :class:`Site <ad.Site>`, the first parameter must
be ``globals()``, because Lino is going to automatically set certain
Django settings. For example

- `DATABASES 
  <https://docs.djangoproject.com/en/dev/ref/settings/#databases>`_ :
  djangosite sets this to a sqlite on a file `default.db` in your 
  :attr:`project_dir <djangosite.Site.project_dir>`.
  
- `INSTALLED_APPS
  <https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps>`_
  
Which simply means that if you want to modify one of these, do it
*after* instantiating your :setting:`SITE`).

The optional second positional argument should be the value of your
original :setting:`INSTALLED_APPS` (to which Lino will automatically
add some).  If you don't specifiy this argument, then you should
specify your installed apps by overriding
:meth:`ad.Site.get_installed_apps`.

Besides this you can override any class argument using a keyword
argment of same name:

- :attr:`ad.Site.title`
- :attr:`ad.Site.verbose_name`

You've maybe heard that it is not allowed to modify Django's settings
once it has started.  But there's nothing illegal with this here
because this happens before Django has seen your :xfile:`settings.py`.

Lino does more than this. It will for example read the `__file__
<http://docs.python.org/2/reference/datamodel.html#index-49>`__
attribute of this, to know where your :file:`settings.py` is in the
file system.


Why
===

The basic idea is to keep local :xfile:`settings.py` files small and
to delegate the responsibility of maintaining default values for
Django settings to the application developer.



.. _djangosite_local:

The ``djangosite_local.py`` file
================================

The :ref:`djangosite_local.py <djangosite_local>` file is another
technique which Lino adds to plain Django.

When a :class:`ad.Site` gets instantiated, it will try to import an
module named ``djangosite_local``, and if that module exists and has a
function named ``setup_site``, will call this function.  

This mechanism is used on servers where many djangosite sites are
running to provide local server-wide default settings.
