==================
Application Design
==================

.. currentmodule:: ad

The :mod:`lino.ad` module is a shortcut to those parts of Lino which
are used in your :xfile:`settings.py` files and in the
:xfile:`__init__.py` files of your apps.  The name ``ad`` stands for
"Application Design".  Application design happens **during** the
import of your Django settings and **before** your models are
imported.

Plugins
-------

A minimal :xfile:`__init__.py` file of a Django app::

    from lino import ad, _

    class Plugin(ad.Plugin):

        verbose_name = _("Places")



The :class:`Site` class is what you are going to instantiate and store
in your :setting:`SITE` setting.

The :class:`Plugin` class is an optional descriptor for every app.


.. function:: configure_plugin(app_label, **kwargs)

  Set one ore several configuration settings of the given plugin.

  This should be called *before instantiating* your :class:`Site`
  class.

  For example to enable :attr:`ml.contacts.Plugin.hide_region` to
  True::

    ad.configure_plugin('contacts', hide_region=True)

  The :func:`configure_plugin` function is a simple interface for
  locally configuring plugins. See :doc:`/admin/settings` for more
  details on this.




The ``Site`` class
------------------


.. class:: Site(settings_globals, user_apps=[], **kwargs)

  Base class for the Site instance to be stored in :setting:`SITE`.

  This may be overridden by the application developer and/or the local
  site administrator.


  .. attribute:: site_prefix

    This must be set if your project is not sitting at the "root" URL 
    of your server.
    It must start *and* end with a *slash*. Default value is ``'/'``. 
    For example if you have::
    
        WSGIScriptAlias /foo /home/luc/mypy/lino_sites/foo/wsgi.py
      
    Then your :xfile:`settings.py` should specify::
    
        site_prefix = '/foo/'
    
    See also :ref:`mass_hosting`.
    

  .. attribute:: help_email

    An e-mail address where users can get help. This is included in
    :xfile:`admin_main.html`.

  .. attribute:: help_url

  .. attribute:: site_config

    This property holds a cached version of the one and only
    :class:`ml.system.SiteConfig` row that holds site-wide
    database-stored parameters.

  .. attribute:: default_user

    Username to be used if a request with 
    no REMOTE_USER header makes its way through to Lino. 
    Which may happen on a development server and if Apache is 
    configured to allow it.
    Used by :mod:`lino.core.auth`.

  .. attribute:: anonymous_user_profile

    The user profile to be assigned to anonymous user.
    

  .. attribute:: the_demo_date

    Specify a fixed date instead of the process startup time to be
    used by :meth:`demo_date`. For example the :ref:`welfare` test
    suite has a fixed demo date because certain tests for generating
    events rely on a fixed date.


  .. attribute:: startup_time

    Don't modify this. 
    It contains the time when this this Site has been instantiated,
    IAW the startup time of this Django process.

  .. attribute:: project_dir

    Read-only.
    Full path to your local project directory. 
    Local subclasses should not override this variable.
    
    The local project directory is where 
    local configuration files are stored:
    
    - Your :xfile:`settings.py`
    - Optionally the :xfile:`manage.py` and :xfile:`urls.py` files
    - Your :xfile:`media` directory
    - Optional local :xfile:`config` and :xfile:`fixtures` directories

  .. attribute:: project_name

    Read-only.
    The leaf name of your local project directory.

  .. attribute:: url

      The URL of the website that describes this application.
      Used e.g. in a :menuselection:`Site --> About` dialog bix.

  .. attribute:: version

    The version number.

  .. attribute:: verbose_name

    Used as display name to end-users at different places.


  .. attribute:: make_missing_dirs

    Set this to `False` if you don't want this Site to automatically
    create missing directories when needed (but to raise an exception
    in these cases, asking you to create it yourself)


  .. method:: get_installed_apps()

    Yield the list of apps to be installed on this site.  This will be
    stored to :setting:`INSTALLED_APPS` when the Site instantiates.  

    Each item must be either a string (unicode being converted to str) or
    a *generator* which will be iterated recursively (again expecting
    either strings or geneortaors of strings).

  .. attribute:: hidden_apps

    A set (or space-spearated string) with the names of apps which should
    *not* get installed even if :setting:`get_installed_apps` returns them.

    Either an empty `set`

  .. method:: get_apps_modifiers(**kw)

    This will be called during Site instantiation (i.e. may not import any
    Django modules) and is expected to return a dict of `app_label` to
    `full_python_path` mappings. The default returns an empty dict.

    These mappings will be applied to the apps returned by
    :meth:`get_installed_apps`. 

    Mapping an app_label to `None` will remove (not install) that app from
    your Site.

    You can use this to override or hide individual apps without changing
    their order. Example::

        def get_apps_modifiers(self, **kw):
            kw.update(debts=None)
            kw.update(courses='lino.modlib.courses')
            kw.update(pcsw='lino_welfare.settings.chatelet.pcsw')
            return kw


  .. attribute:: override_modlib_models

    Internally used. Contains a set of model names that were 
    declared to be overridden.

    See also :func:`dd.is_abstract_model`.

  .. attribute:: django_settings

    This is where the Site stores the `globals()` dictionary of your
    :xfile:`settings.py` file (the one you provided when 
    instantiating the Site object).


  .. attribute:: demo_date

    Compute a date using :func:`atelier.utils.date_offset` based on
    the process startup time (or :attr:`the_demo_date` if this is
    set).

    Used in Python fixtures and unit tests.

  .. attribute:: languages

    The language distribution used on this site.

    This must be either `None` or an iterable of language codes.
    Or a string containing a space-separated suite of language codes.

    Examples::

      languages = "en de fr nl et".split()
      languages = ['en']
      languages = 'en fr'

    See :meth:`apply_languages` for more detailed description.

    The first language in this list will be the site's 
    default language.

    Changing this setting affects your database structure if your
    application uses babel fields, and thus require a :ref:`data
    migration <datamig>`.

    If this is not `None`, Site will set the Django settings 
    `USE_L10N <http://docs.djangoproject.com/en/dev/ref/settings/#use-l10n>`_ 
    and
    `LANGUAGE_CODE <http://docs.djangoproject.com/en/dev/ref/settings/#language-code>`_.


    >>> from django.utils import translation
    >>> from north import TestSite as Site
    >>> from pprint import pprint
    >>> pprint(Site().django_settings)  #doctest: +ELLIPSIS
    {'DATABASES': {'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': '...default.db'}},
     'FIXTURE_DIRS': (),
     'INSTALLED_APPS': ('north', 'djangosite'),
     'LANGUAGES': [],
     'LOCALE_PATHS': (),
     'SECRET_KEY': '20227',
     'SERIALIZATION_MODULES': {'py': 'north.dpy'},
     '__file__': '...'}

    >>> pprint(Site(languages="en fr de").languages)
    (LanguageInfo(django_code='en', name='en', index=0, suffix=''),
     LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr'),
     LanguageInfo(django_code='de', name='de', index=2, suffix='_de'))

    >>> pprint(Site(languages="de-ch de-be").languages)
    (LanguageInfo(django_code='de-ch', name=u'de_CH', index=0, suffix=''),
     LanguageInfo(django_code='de-be', name=u'de_BE', index=1, suffix='_de_BE'))

    If we have more than languages en-us and en-gb *on a same Site*, 
    then it is not allowed to specify just "en". 
    But in most cases it is allowed to just say "en", which will 
    mean "the English variant used on this Site".

    >>> site = Site(languages="en-us fr de-be de")
    >>> pprint(site.languages)
    (LanguageInfo(django_code='en-us', name=u'en_US', index=0, suffix=''),
     LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr'),
     LanguageInfo(django_code='de-be', name=u'de_BE', index=2, suffix='_de_BE'),
     LanguageInfo(django_code='de', name='de', index=3, suffix='_de'))

    >>> pprint(site.language_dict)
    {'de': LanguageInfo(django_code='de', name='de', index=3, suffix='_de'),
     u'de_BE': LanguageInfo(django_code='de-be', name=u'de_BE', index=2, suffix='_de_BE'),
     'en': LanguageInfo(django_code='en-us', name=u'en_US', index=0, suffix=''),
     u'en_US': LanguageInfo(django_code='en-us', name=u'en_US', index=0, suffix=''),
     'fr': LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr')}

    >>> pprint(site.django_settings['LANGUAGES'])  #doctest: +ELLIPSIS
    [('de', 'German'), ('fr', 'French')]


  .. method:: field2kw(obj,name,**known_values)

    Examples:

    >>> from north import TestSite as Site
    >>> from atelier.utils import AttrDict
    >>> def testit(site_languages):
    ...     site = Site(languages=site_languages)
    ...     obj = AttrDict(site.babelkw('name',de="Hallo",en="Hello",fr="Salut"))
    ...     return site,obj


    >>> site, obj = testit('de en')
    >>> site.field2kw(obj, 'name')
    {'de': 'Hallo', 'en': 'Hello'}

    >>> site, obj = testit('fr et')
    >>> site.field2kw(obj, 'name')
    {'fr': 'Salut'}

        
  .. method:: babelitem(*args,**values)

    Given a dictionary with babel values, return the 
    value corresponding to the current language.

    This is available in templates as a function `tr`.

    >>> kw = dict(de="Hallo", en="Hello", fr="Salut")

    >>> from north import TestSite as Site
    >>> from django.utils import translation

    A Site with default language "de":

    >>> site = Site(languages="de en")
    >>> tr = site.babelitem
    >>> with translation.override('de'):
    ...    tr(**kw)
    'Hallo'

    >>> with translation.override('en'):
    ...    tr(**kw)
    'Hello'

    If the current language is not found in the specified `values`,
    then it returns the site's default language ("de" in our example):

    >>> with translation.override('jp'):
    ...    tr(en="Hello",de="Hallo",fr="Salut")
    'Hallo'

    Another way is to specify an explicit default value using a
    positional argument. In that case the language's default language
    doesn'n matter:

    >>> with translation.override('jp'):
    ...    tr("Hello",de="Hallo",fr="Salut")
    'Hello'

    >>> with translation.override('de'):
    ...     tr("Hello",de="Hallo",fr="Salut")
    'Hallo'

    You may not specify more than one default value:

    >>> tr("Hello","Hallo")
    Traceback (most recent call last):
    ...
    ValueError: ('Hello', 'Hallo') is more than 1 default value.




  .. attribute:: hidden_languages

    A string of django codes of languages that should be hidden.

    :ref:`welfare` uses this because the demo database has 4
    languages, but `nl` is currently hidden bu default.



  .. attribute:: migration_class

    If you maintain a data migrator module for your application, 
    specify its name here.

    See :ref:`datamig` and/or :func:`north.dpy.install_migrations`.



  .. attribute:: loading_from_dump

    This is normally `False`, except when the process is loading data from
    a Python dump.

    The Python dump then calls :func:`north.dpy.install_migrations` which
    sets this to `True`.

    Application code should not change this setting (except for certain
    special test cases).



  .. method:: setup_choicelists()

    This is a hook for code to be run *after* all plugins have been
    instantiated and *before* the models are being discovered.

    This is especially useful for redefining your application's
    ChoiceLists.

    Especially used to define application-specific
    :class:`UserProfiles <lino.core.perms.UserProfiles>`.

    Lino by default has two user profiles "User" and "Administrator",
    defined in :mod:`lino.core.perms`.

    Application developers who use group-based requirements can
    override this in their application's :xfile:`settings.py` to
    provide a default list of user profiles for their application.

    See the source code of :mod:`lino.projects.presto` or
    :mod:`lino_welfare.settings` for a usage example.

    Local site administrators may again override this in their
    :xfile:`settings.py`.

    Note that you may not specify values longer than `max_length` when
    redefining your choicelists.  This limitation is because these
    redefinitions happen at a moment where database fields have
    already been instantiated, so it is too late to change their
    max_length.  Note that this limitation is only for the *values*,
    not for the names or texts of choices.

  .. method:: get_installed_apps

    This method is expected to yield the list of strings
    to be stored into Django's :setting:`INSTALLED_APPS` setting.


  .. attribute:: config_id

    The primary key of the one and only `SiteConfig` instance of this
    SITE. Default value is 1.

    This is Lino's equivalent of Django's :setting:`SITE_ID` setting.
    Lino applications don't need ``django.contrib.sites`` (`The "sites"
    framework
    <https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_) because
    this functionality is integral part of :mod:`lino.modlib.system`.

  .. attribute:: verbose_client_info_message

    Set this to True if actions should send debug messages to the client.
    These will be shown in the client's Javascript console only.

  .. attribute:: is_demo_site

    When this is `True`, then this site runs in "demo" mode.     
    "Demo mode" means:
    
    - the welcome text for anonymous users says "This demo site has X 
      users, they all have "1234" as password", 
      followed by a list of available usernames.
    
    Default value is `True`.
    On a production site you will of course set this to `False`.
    
    See also :attr:`demo_fixtures`.

  .. attribute:: demo_fixtures

    The list of fixtures to be loaded by the :manage:`initdb_demo`
    command.


  .. attribute:: time_format_extjs
    """
    Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.
    """

  .. attribute:: date_format_extjs
    """
    Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.
    """

  .. attribute:: alt_date_formats_extjs

    """
    Alternative date entry formats accepted by ExtJS Date widgets.
    """


  .. attribute:: use_davlink

    No longer used. Replaced by :class:`lino.modlib.davlink`.

    Set this to `True` if this site should feature WebDAV-enabled links
    using :ref:`davlink`.

  .. attribute:: use_eidreader

    No longer used. Replaced by :class:`lino.modlib.beid`.

    Set this to `True` if this site should feature using :ref:`eidreader`.


  .. attribute:: auto_configure_logger_names

    A string with a space-separated list of logger names to be
    automatically configured. See :mod:`lino.utils.log`.

    .. setting:: use_java

    A site-wide option to disable everything that needs Java.  Note that
    it is up to the apps which include Java applications to respect this
    setting. Usage example is :mod:`lino.modlib.beid`.

  .. attribute:: user_model

    Most Lino application wil set this to ``"users.User"`` if you use
    `lino.modlib.users`.

    Default value us `None`, meaning that this site has no user management
    (feature used by e.g. :mod:`lino.test_apps.1`)

    Set this to ``"auth.User"`` if you use `django.contrib.auth` instead of
    `lino.modlib.users` (not tested).


  .. attribute:: remote_user_header
    
    The name of the header (set by the web server) that Lino should
    consult for finding the user of a request.  The default value `None`
    means that http authentication is not used.  Apache's default value is
    ``"REMOTE_USER"``.


  .. attribute:: ldap_auth_server

    This should be a string with the domain name and DNS (separated by a
    space) of the LDAP server to be used for authentication.  Example::

      ldap_auth_server = 'DOMAIN_NAME SERVER_DNS'

    .. setting:: auth_middleware

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

  .. setting:: plain_prefix

    The prefix to use for "plain html" URLs.
    Default value is ``'plain'``.

    TODO: convert `plain_prefix` to a `url_prefix` setting on the
    `lino.modlib.plain` App.

    Exactly one of :setting:`admin_prefix` and :setting:`plain_prefix`
    must be empty.


  .. setting:: preview_limit
    
    Default value for the :attr:`preview_limit
    <lino.core.tables.AbstractTable.preview_limit>` parameter of all
    tables who don't specify their own one.  Default value is 15.


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



The ``Plugin`` class
--------------------

The basic usage is to write in your :xfile:`__init__.py` file::

    from lino import ad, _

    class Plugin(ad.Plugin):
        verbose_name = _("Contacts")




.. class:: Plugin

    The base class for all plugins.

    Every Django app may define a class object called "Plugin" in
    its :xfile:`__init__.py` module (not in the :xfile:`models.py` module).

    Plugins get instiantiated exactly once when the :class:`Site`
    object instantiates (i.e. before Django settings are ready).

    All plugins are globally accessible 
    in :data:`dd.apps` using the `app_label` as key.

  .. attribute:: verbose_name

    The name of this app, as shown to the user. This can be
    translatable. 


  .. attribute:: extends_models

    If specified, a list of model names for which this app provides a
    subclass.
    
    For backwards compatibility this has no effect
    when :setting:`override_modlib_models` is set.

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
    but while developing, it may be easier to set it to `False`, which means 
    that each file is built upon need (when a first request comes in).
    
    The default value `None` means that Lino decides automatically 
    during startup:
    it becomes `False` if
    either :func:`lino.core.dbutils.is_devserver` returns True
    or setting:`DEBUG` is set.

  .. attribute:: use_experimental_features

    Whether to include "experimental features".


  .. attribute:: site_config_defaults

    Default values to be used when creating the 
    :class:`ml.system.SiteConfig` instance.
    
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


  .. method:: configure(self, **kw)

    Set the given parameter(s) of this Plugin instance.
    Any number of parameters can be specified as keyword arguments.

    Raise an exception if caller specified a key that does not
    have a corresponding attribute.

  .. method:: welcome_text()

    Text to display in a console window when this Site starts.

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

    Yield a sequence of "items" to be rendered in
    :xfile:`admin_main.html`.

  .. method:: get_system_note_recipients(self, ar, obj, silent)

    Return or yield a list of recipients
    (i.e. strings "Full Name <name@example.com>" )
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
