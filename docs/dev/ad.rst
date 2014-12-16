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

Lino defines two classes :class:`Site` and :class:`Plugin` which are
heavily used to do lots of magic and to make apps more pleasant to
configure.

.. contents:: 
   :local:
   :depth: 2


.. note:: 

  This is a tested document. You can test it using::

    $ python setup.py test -s tests.DocsTests.test_docs

.. 
  >>> import os
  >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
  ...   'lino.projects.docs.settings.demo'
  >>> from lino.runtime import *



The ``Site`` class
------------------

.. class:: Site(settings_globals, user_apps=[], **kwargs)


  .. attribute:: remote_user_header
    
    The name of the header (set by the web server) that Lino should
    consult for finding the user of a request.  The default value `None`
    means that http authentication is not used.  Apache's default value is
    ``"REMOTE_USER"``.


  .. attribute:: ldap_auth_server

    This should be a string with the domain name and DNS (separated by a
    space) of the LDAP server to be used for authentication.  Example::

      ldap_auth_server = 'DOMAIN_NAME SERVER_DNS'

  .. attribute:: auth_middleware

    Override used Authorisation middlewares with supplied tuple of
    middleware class names.

    If None, use logic described in :doc:`/topics/auth`
  


  .. attribute:: project_model

    Deprecated because this is an obsolete pattern.

    Optionally set this to the <applabel.ModelName> of a model used as
    "central project" in your application.  Which concretely means that
    certain other models like notes.Note, outbox.Mail, ... have an
    additional ForeignKey to this model.



  .. attribute:: admin_prefix

    The prefix to use for Lino "admin mode"
    (i.e. the "admin main page" with a pull-down "main menu").

    TODO: convert `admin_prefix` to a `url_prefix` setting on the
    `lino.modlib.extjs` plugin.

    The default value is an empty string, resulting in a website whose
    root url shows the admin mode.

    Note that unlike Django's `MEDIA_URL
    <https://docs.djangoproject.com/en/dev/ref/settings/#media-url>`__
    setting, this must not contain any slash.

    If this is nonempty, then your site features a "web content mode": the
    root url renders "web content" defined by :mod:`lino.modlib.pages`.
    The usual value in that case is ``admin_prefix = "admin"``.

    See also

    - `telling Django to recognize a different application root url
      <http://groups.google.com/group/django-users/browse_thread/thread/c95ba83e8f666ae5?pli=1>`__
    - `How to get site's root path in Django 
      <http://groups.google.com/group/django-users/browse_thread/thread/27f035aa8e566af6>`__
    - `#8906 django.contrib.auth settings.py URL's aren't portable <https://code.djangoproject.com/ticket/8906>`__
    - `Changed the way URL paths are determined 
      <https://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#ChangedthewayURLpathsaredetermined>`__

  .. attribute:: plain_prefix

    The prefix to use for "plain html" URLs.
    Default value is ``'plain'``.

    TODO: convert `plain_prefix` to a `url_prefix` setting on the
    `lino.modlib.plain` App.

    Exactly one of :attr:`admin_prefix` and :attr:`plain_prefix`
    must be empty.


  .. attribute:: preview_limit
    
    Default value for the :attr:`preview_limit
    <dd.AbstractTable.preview_limit>` parameter of all tables who
    don't specify their own one.  Default value is 15.


  .. attribute:: start_year

    An integer with the calendar year in which this site starts working.
    Used e.g. 
    by :mod:`lino.modlib.ledger.utils`
    to fill the default list of FixcalYears.
    Or by :mod:`lino.modlib.ledger.fixtures.mini`
    to generate demo invoices.


  .. attribute:: uppercase_last_name

    Whether last name of persons should (by default) be printed with
    uppercase letters.  See :mod:`lino.test_apps.human`

  .. method:: setup_plugins(self)

    This method is called exactly once during site startup, after
    :meth:`load_plugins` and before models are being populated.

  .. method:: do_site_startup(self)

    This method is called exactly once during site startup,
    just between the pre_startup and the post_startup signals.
    A hook for subclasses.

    If you override it, don't forget to call the super method
    which calls :meth:`Plugin.on_site_startup` for each
    installed plugin.

  .. method:: get_settings_subdirs(self, subdir_name)

    Yield all (existing) directories named `subdir_name` of this
    site's project directory and it's inherited project
    directories.




  .. attribute:: legacy_data_path

    Used by custom fixtures that import data from some legacy
    database.

  .. attribute:: never_build_site_cache

    Set this to `True` if you want that Lino never (re)builds the site
    cache, even when asked.  This can be useful on a development
    server when you are debugging directly on the generated
    :xfile:`lino*.js`.  Or for certain unit test cases.

  .. attribute:: build_js_cache_on_startup

    Whether the Javascript cache files should be built on startup for
    all user profiles and languages.
    
    On a production server this should be `True` for best performance,
    but often this is not necessary, so default value is `False`,
    which means that each file is built upon need (when a first
    request comes in).
    
    You can also set it to `None`, which means that Lino decides
    automatically during startup: it becomes `False` if either
    :func:`lino.core.dbutils.is_devserver` returns True or
    setting:`DEBUG` is set.

  .. attribute:: use_experimental_features

    Whether to include "experimental features".


  .. attribute:: site_config_defaults

    Default values to be used when creating the :attr:`site_config`.
    
    Usage example::
    
      site_config_defaults = dict(default_build_method='appypdf')
      


  .. attribute:: show_internal_field_names

    Whether the internal field names should be visible.  Default is
    `False`.  ExtUI implements this by prepending them to the tooltip,
    which means that :attr:`use_quicktips` must also be `True`.

  .. attribute:: trusted_templates

    Set this to True if you are sure that the users of your site won't try to 
    misuse Jinja's capabilities.

  .. attribute:: allow_duplicate_cities

    In a default configuration (when :attr:`allow_duplicate_cities` is
    False), Lino declares a UNIQUE clause for :class:`Places
    <lino.modlib.countries.models.Places>` to make sure that your
    database never contains duplicate cities.  This behaviour mighr
    disturb e.g. when importing legacy data that did not have this
    restriction.  Set it to True to remove the UNIQUE clause.
    
    Changing this setting might affect your database structure and
    thus require a :doc:`/topics/datamig` if your application uses
    :mod:`lino.modlib.countries`.


  .. method:: using_text()

    Text to display in a console window when Lino starts.

  .. method:: get_used_libs(html=None)

    Yield a list of (name, version, url) tuples describing the
    third-party software used on this Site.

    This function is used by :meth:`using_text` which is used by
    :meth:`welcome_text`.

  .. method:: site_version()

    Used in footnote or header of certain printed documents.


  .. method:: on_site_startup(site)

    This will be called exactly once, when models are ready.

  .. method:: get_letter_date_text(today=None)

    Returns a string like "Eupen, den 26. August 2013".

  .. method:: get_admin_main_items(ar)

    Expected to yield a sequence of "items" to be rendered on the home
    page (:xfile:`admin_main.html`).

    Every item is expected to be a :class:`dd.Table` or a
    :class:`dd.VirtualTable`. These tables are rendered in that order,
    with a limit of :attr:`dd.AbstractTable.preview_limit` rows.


  .. method:: get_system_note_recipients(self, ar, obj, silent)

    Return or yield a list of recipients
    (i.e. strings like "John Doe  <john@example.com>" )
    to be notified by email about a system note issued
    by action request `ar` about the object instance `obj`.

    Default behaviour is to simply forward it to the `obj`'s
    :meth:`get_system_note_recipients
    <dd.Model.get_system_note_recipients>`, but here is a hook to
    define local exceptions to the application specific default rules.

  .. method:: welcome_html(self, ui=None)

    Return a HTML version of the "This is APPLICATION
    version VERSION using ..." text. to be displayed in the
    About dialog, in the plain html footer, and maybe at other
    places.

  .. method:: get_db_overview_rst(self)

    Return a reStructredText-formatted "database overview" report.
    Used by test cases in tested documents.

  .. method:: site_header(self)

    Used in footnote or header of certain printed documents.

    The convention is to call it as follows from an appy.pod template
    (use the `html` function, not `xhtml`)
    ::

      do text
      from html(settings.SITE.site_header())

    Note that this is expected to return a unicode string possibly
    containing valid HTML (not XHTML) tags for formatting.

  .. method:: get_default_required(**kwargs):
    
    Return a dict with the default value for the
    :attr:`dd.Actor.required` attribute of every actor.


The ``Plugin`` class
--------------------


.. class:: Plugin

  .. attribute:: verbose_name

    The name of this app, as shown to the user. This can be
    translatable. 



  .. attribute:: media_base_url

    Remote URL base for media files.


  .. attribute:: media_root
    Local path where third-party media files are installed.

    Only used if this app has :attr:`media_base_url` empty and
    :attr:`media_name` non-empty, *and* if the :xfile:`media`
    directory has no entry named :attr:`media_name`.

  .. attribute:: media_name

    Either `None` (default) or a non-empty string with the name of the
    subdirectory of your :xfile:`media` directory which is expected to
    contain media files for this app.

    `None` means that there this app has no media files of her own.

    Best practice is to set this to the `app_label`.  Will be ignored
    if :attr:`media_base_url` is nonempty.

  .. attribute:: url_prefix

    The url prefix under which this app should ask to
    install its url patterns.

  .. attribute:: site_js_snippets

    List of js snippets to be injected into the `lino_*.js` file.

  .. attribute:: extends_models

    If specified, a list of model names for which this app provides a
    subclass.
    
  .. method:: configure(self, **kw)

    Set the given parameter(s) of this Plugin instance.
    Any number of parameters can be specified as keyword arguments.

    Raise an exception if caller specified a key that does not
    have a corresponding attribute.



Configuring plugins
-------------------


.. function:: configure_plugin(app_label, **kwargs)

  Set one ore several configuration settings of the given plugin.

  The :func:`configure_plugin` function is a simple interface for
  locally configuring plugins. 

  This should be called *before instantiating* your :class:`Site`
  class.

  For example to set :attr:`ml.contacts.Plugin.hide_region` to
  True::

    ad.configure_plugin('contacts', hide_region=True)

  See :doc:`/admin/settings` for more details.


Using plugins
-------------

All plugins are globally accessible under :data:`dd.apps` using the
`app_label` as key.


