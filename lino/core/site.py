# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre.
# License: BSD, see LICENSE for more details.

"""Defines the :class:`Site` class. For an overview see
:doc:`/dev/site` and :doc:`/dev/plugins` .

.. This document is part of the Lino test suite. You can test only
    this document using::

        $ python setup.py test -s tests.CoreTests.test_site
        $ python lino/core/site.py

    doctest init:
    >>> import lino
    >>> lino.startup('lino.projects.std.settings_test')

"""
from __future__ import unicode_literals, print_function
from future import standard_library
standard_library.install_aliases()
from builtins import map
import six
# str = six.text_type
from builtins import str
# from past.builtins import basestring
# from builtins import object

import os
from os.path import normpath, dirname, join, isdir, relpath, exists
import inspect
import datetime
import warnings
import collections
import threading
from importlib import import_module
from urllib.parse import urlencode
from lino import AFTER17
if AFTER17:
    from django.apps import AppConfig

from unipath import Path
from atelier.utils import AttrDict, date_offset, tuple_py2
from atelier import rstgen

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
# from django.core.exceptions import ImproperlyConfigured

from lino.core.plugin import Plugin

from lino import assert_django_code, DJANGO_DEFAULT_LANGUAGE
from lino.utils.xmlgen.html import E
from lino.utils.html2text import html2text
from lino.core.exceptions import ChangedAPI
# from .roles import SiteUser

startup_rlock = threading.Lock()  # Lock() or RLock()?

LanguageInfo = collections.namedtuple(
    'LanguageInfo', ('django_code', 'name', 'index', 'suffix'))
"""
A named tuple with four fields:

- `django_code` -- how Django calls this language
- `name` --        how Lino calls it
- `index` --       the position in the :attr:`Site.languages` tuple
- `suffix` --      the suffix to append to babel fields for this language

"""


def to_locale(language):
    """Simplified copy of `django.utils.translation.to_locale`, but we
    need it while the `settings` module is being loaded, i.e. we
    cannot yet import django.utils.translation.  Also we don't need
    the to_lower argument.

    """
    p = language.find('-')
    if p >= 0:
        # Get correct locale for sr-latn
        if len(language[p + 1:]) > 2:
            return language[:p].lower() + '_' \
                + language[p + 1].upper() + language[p + 2:].lower()
        return language[:p].lower() + '_' + language[p + 1:].upper()
    else:
        return language.lower()


def class2str(cl):
    return cl.__module__ + '.' + cl.__name__

gettext_noop = lambda s: s

PLUGIN_CONFIGS = {}


def configure_plugin(app_label, **kwargs):
    """Set one ore several configuration settings of the given plugin
    *before* the :setting:`SITE` has been instantiated.
    See :doc:`/dev/plugins`.

    """
    # if PLUGIN_CONFIGS is None:
    #     raise ImproperlyConfigured(
    #         "Tried to call configure_plugin after Site instantiation")
    cfg = PLUGIN_CONFIGS.setdefault(app_label, {})
    cfg.update(kwargs)


# from django.db.models.fields import NOT_PROVIDED
class NOT_PROVIDED(object):
    pass


class Site(object):
    """The base class for a Lino application.  This class is designed to
    be overridden by both application developers and local site
    administrators.  Your :setting:`SITE` setting is expected to
    contain an instance of a subclass of this.

    .. attribute:: plugins

        An :class:`AttrDict` object with one entry for each installed
        app, mapping the `app_label` of every plugin to the
        corresponding :class:`lino.core.plugin.Plugin` instance.

        This attribute is automatically filled by Lino and available as
        :attr:`dd.plugins <lino.api.dd>` already before Django starts to
        import :xfile:`models.py` modules.


    .. attribute:: modules

        Old name for :attr:`models`.  Deprecated.

    .. attribute:: models

        An :class:`AttrDict <atelier.utils.AttrDict>` which maps every
        installed `app_label` to the corresponding :xfile:`models.py`
        module object.

        This is also available as the shortcut :attr:`rt.models
        <lino.api.rt.models>`.

        See :doc:`/dev/plugins`



    .. attribute:: LANGUAGE_CHOICES
    
        A tuple in the format expected by Django's `choices
        <https://docs.djangoproject.com/en/1.7/ref/models/fields/#choices>`__
        attribute, used e.g. by :class:`LanguageField
        <lino.utils.mldbc.fields.LanguageField>`. It's content is
        automatically populated from :attr:`languages` and application
        code should not change it's value.

    """

    auto_fit_column_widths = True
    """The default value for the
    :attr:`auto_fit_column_widths<lino.core.tables.AbstractTable.auto_fit_column_widths>`
    of tables in this application.

    """

    confdirs = None
    """This attribute is available only after site startup.  See
    :mod:`lino.utils.config`.
    """

    kernel = None
    """
    This attribute is available only after :meth:`startup`.
    See :mod:`lino.core.kernel`.

    """

    ui = None
    """
    Deprecated alias for :attr:`kernel`.

    """

    readonly = False
    """Setting this to `True` turns this site in a readonly site.  This
    means that :setting:`DATABASES` must point to the
    :setting:`DATABASES` of some other (non-readonly) site, and that
    :manage:`initdb` will do nothing.

    """

    the_demo_date = None
    """A hard-coded constant date to be used as reference by :meth:`today`
    and :meth:`demo_date`. For example many demo databases have this
    set because certain tests rely on a constant reference date.

    """

    title = None
    """The title of this web site to appear in the browser window.  If
    this is None, Lino will use :attr:`verbose_name` as default value.

    """

    verbose_name = "yet another Lino application"
    """The name of this application, to be displayed to end-users at
    different places.

    Note the difference between :attr:`title` and
    :attr:`verbose_name`:

    - :attr:`title` may be None, :attr:`verbose_name` not.

    - :attr:`title` is used by the
      :srcref:`index.html <lino/modlib/extjs/config/extjs/index.html>` for
      :mod:`lino.modlib.extjs`.

    - :attr:`title` and :attr:`verbose_name` are used by
      :xfile:`admin_main.html` to generate the fragments "Welcome to the
      **title** site" and "We are running **verbose_name** version
      **x.y**"  (the latter only if :attr:`version` is set).

    - :meth:`site_version` uses :attr:`verbose_name` (not :attr:`title`)

    IOW, the :attr:`title` is rather for usage by local system
    administrators, while the :attr:`verbose_name` is rather for usage
    by application developers.

    """

    version = None
    "The version number."

    url = None
    """
    The URL of the website that describes this application.
    Used e.g. in a :menuselection:`Site --> About` dialog box.
    """

    server_url = None
    """The "official" URL used by "normal" users when accessing this Lino
    site. This is used by templates such as the email sent by
    :class:`lino.modlib.notify.Notification`

    """

    obj2text_template = "*{0}*"
    """The format template to use when rendering a ForeignKey as plain
    text.

    Note: reSTructuredText uses *italic* and **bold**.  Changing this
    can cause lots of trivial failures in test suites.  It is also
    used by :mod:`lino.modlib.notify` when generating the mail body.

    """
    make_missing_dirs = True
    """
    Set this to `False` if you don't want this Site to automatically
    create missing directories when needed (but to raise an exception
    in these cases, asking you to create it yourself)

    """
    userdocs_prefix = ''

    project_name = None
    """A nickname for this project. This is used to set :attr:`cache_dir`
    and therefore should be unique for all Lino projects on a given
    machine.

    If this is None, Lino will find a default value by splitting
    :attr:`project_dir` and taking the last part (or the second-last
    if the last part is 'settings'.

    """

    cache_dir = None
    """The directory where Lino will create temporary data for this
    project, including the :xfile:`media` directory and the
    :xfile:`default.db` file.

    This is either the same as :attr:`project_dir` or (if
    :envvar:`LINO_CACHE_ROOT` is set), will be set to
    :envvar:`LINO_CACHE_ROOT` + :attr:`project_name`.

    """

    project_dir = None
    """Full path to your local project directory.

    Lino automatically sets this to the directory of the
    :xfile:`settings.py` file (or however your
    :envvar:`DJANGO_SETTINGS_MODULE` is named).
    It is recommended to not override this variable.

    Note that when using a *settings package*, :attr:`project_dir`
    points to the :file:`settings` subdir of what we would intuitively
    consider the project directory.

    If the :attr:`project_dir` contains a :xfile:`config` directory,
    this will be added to the config search path.

    """

    languages = None
    """The language distribution used on this site.  It has its own
    chapter :doc:`/dev/languages` in the Developers Guide.

    """

    not_found_msg = '(not installed)'

    django_settings = None
    """This is a reference to the `globals()` dictionary of your
    :xfile:`settings.py` file (the one you provided when instantiating
    the Site object).

    """

    startup_time = None
    """
    The time when this Site has been instantiated,
    in other words the startup time of this Django process.
    Don't modify this.

    """

    plugins = None

    modules = models = AttrDict()

    top_level_menus = [
        ("master", _("Master")),
        ("main", None),
        ("reports", _("Reports")),
        ("config", _("Configure")),
        ("explorer", _("Explorer")),
        ("site", _("Site")),
    ]
    "The list of top-level menu items. See :meth:`setup_menu`."

    is_local_project_dir = False
    """Contains `True` if this is a "local" project.  For local projects,
    Lino checks for local fixtures and config directories and adds
    them to the default settings.

    This is automatically set when a :class:`Site` is instantiated.

    """

    ignore_model_errors = False
    """Not yet sure whether this is needed. Maybe when generating
    documentation.

    """

    loading_from_dump = False
    """Whether the process is currently loading data from a Python dump.

    When loading from a python dump, application code should not
    generate certain automatic data because that data is also part of
    the dump.

    This is normally `False`, but a Python dump created with
    :manage:`dump2py` explicitly calls :meth:`install_migrations`
    which sets this to `True`.

    Application code should not change this setting except for certain
    special test cases.

    """

    # see docs/settings.rst
    migration_class = None
    """
    If you maintain a data migrator module for your application, 
    specify its name here.

    See :ref:`datamig` and/or :func:`lino.utils.dpy.install_migrations`.

    """

    hidden_languages = None
    """A string with a space-separated list of django codes of languages
    that should be hidden.

    :ref:`welfare` uses this because the demo database has 4
    languages, but `nl` is currently hidden bu default.

    """

    BABEL_LANGS = tuple()

    partners_app_label = 'contacts'
    """
    Temporary setting, see :ref:`polymorphism`.
    """

    # three constants used by lino_xl.lib.workflows:
    max_state_value_length = 20
    max_action_name_length = 50
    max_actor_name_length = 100

    trusted_templates = False
    """
    Set this to True if you are sure that the users of your site won't try to
    misuse Jinja's capabilities.

    """

    allow_duplicate_cities = False
    """In a default configuration (when :attr:`allow_duplicate_cities` is
    False), Lino declares a UNIQUE clause for :class:`Places
    <lino_xl.lib.countries.models.Places>` to make sure that your
    database never contains duplicate cities.  This behaviour mighr
    disturb e.g. when importing legacy data that did not have this
    restriction.  Set it to True to remove the UNIQUE clause.
    
    Changing this setting might affect your database structure and
    thus require a :doc:`/topics/datamig` if your application uses
    :mod:`lino_xl.lib.countries`.

    """

    uid = 'myuid'
    """A universal identifier for this Site.  This is needed when
    synchronizing with CalDAV server.  Locally created calendar
    components in remote calendars will get a UID based on this
    parameter, using ``"%s@%s" % (self.pk, settings.SITE.kernel)``.
    
    The default value is ``'myuid'``, and you should certainly
    override this on a production server that uses remote calendars.

    """

    project_model = None
    """
    Optionally set this to the <applabel.ModelName> of a model used as
    "central project" in your application.  Which concretely means that
    certain other models like notes.Note, outbox.Mail, ... have an
    additional ForeignKey to this model.

    """

    user_model = None
    """If :mod:`lino.modlib.users` is installed, this holds a reference to
    the model class which represents a user of the system. Default
    value is `None`, meaning that this application has no user
    management.  See also :meth:`set_user_model`

    """

    # use_auth = True
    # """Whether this site uses authentication.  If this is set to `False`,
    # all requests are anonymous (as if :attr:`user_model` was `None`).
    # This is ignored when :attr:`user_model` is `None`.
    # """

    auth_middleware = None
    """
    Override used Authorisation middlewares with supplied tuple of
    middleware class names.

    If None, use logic described in :doc:`/topics/auth`
  

    """

    workflows_module = None
    """The full Python path of the **workflows module** to be used on
    this site.
    """
    
    user_profiles_module = None
    """The full Python path of the **user profiles module** to be used on
    this site.

    This must be set if you want to enable permission control based on
    user roles defined in :attr:`Permittable.required_roles
    <lino.core.permissions.Permittable.required_roles>` and
    :attr:`UserProfile.role
    <lino.modlib.users.choicelists.UserProfile.role>`.

    Default value is `None`, meaning that role-based permission
    control is inactive: every user can see everything.

    If set, Lino will import this module during site startup. It is
    expected to define application-specific user roles (if necessary)
    and to fill the :class:`UserProfiles
    <lino.modlib.users.choicelists.UserProfiles>` choicelist.

    For example::

        class Site(Site):
            user_profiles_module = 'lino.modlib.users.roles'

    Examples of such user profiles modules are
    :mod:`lino.modlib.users.roles` and
    :mod:`lino.projects.presto.roles`.

    """

    legacy_data_path = None
    """
    Used by custom fixtures that import data from some legacy
    database.

    """

    propvalue_max_length = 200
    """
    Used by :mod:`lino_xl.lib.properties`.
    """

    show_internal_field_names = True
    """Whether the internal field names should be visible.  ExtUI
    implements this by prepending them to the tooltip, which means
    that :attr:`use_quicktips` must also be `True`.  Default is
    `True`.

    """

    never_build_site_cache = False
    """Set this to `True` if you want that Lino never (re)builds the site
    cache, even when asked.  This can be useful on a development
    server when you are debugging directly on the generated
    :xfile:`lino*.js`.  Or for certain unit test cases.

    """

    build_js_cache_on_startup = False
    """Whether the Javascript cache files should be built on startup for
    all user profiles and languages.
    
    On a production server this should be `True` for best performance,
    but often this is not necessary, so default value is `False`,
    which means that each file is built upon need (when a first
    request comes in).
    
    You can also set it to `None`, which means that Lino decides
    automatically during startup: it becomes `False` if either
    :func:`lino.core.utils.is_devserver` returns True or
    setting:`DEBUG` is set.

    """

    keep_erroneous_cache_files = False
    """When some exception occurs during
    :meth:`lino.core.kernel.Kernel.make_cache_file`, Lino usually
    removes the partly generated file to make sure that it will try to
    generate it again (and report the same error message) for every
    subsequent next request.

    Set this to `True` if you need to see the partly generated cache
    file.  **Don't forget to remove this** when you have inspected the
    file and fixed the reason of the exception, because if this is
    `True` and some next exception occurs (which will happen sooner or
    later), then all subsequent requests will usually end up to the
    user with a blank screen and (if they notice it), a message
    :message:`TypeError: Lino.main_menu is undefined` in their
    Javascript console.

    """

    use_java = True
    """
    A site-wide option to disable everything that needs Java.  Note that
    it is up to the apps which include Java applications to respect this
    setting. Usage example is :mod:`lino_xl.lib.beid`.

    """

    use_experimental_features = False
    """Whether to include "experimental features".
    """
    site_config_defaults = {}
    """
    Default values to be used when creating the :attr:`site_config`.
    
    Usage example::
    
      site_config_defaults = dict(default_build_method='appypdf')
      

    """

    # default_build_method = "appypdf"
    # default_build_method = "appyodt"
    # default_build_method = "wkhtmltopdf"
    default_build_method = None
    """The default build method to use when rendering printable documents.

    This is the last default value, used only when
    :attr:`default_build_method
    <lino.modlib.system.models.SiteConfig.default_build_method>` in
    :class:`SiteConfig <lino.modlib.system.models.SiteConfig>` is
    empty.

    """

    is_demo_site = True
    """When this is `True`, then this site runs in "demo" mode.  "Demo
    mode" means:
    
    - the welcome text for anonymous users says "This demo site has X
      users, they all have "1234" as password", followed by a list of
      available usernames.
    
    Default value is `True`.  On a production site you will of course
    set this to `False`.
    
    See also :attr:`demo_fixtures`.

    """

    demo_email = 'demo@example.com'

    demo_fixtures = ['std', 'demo', 'demo2']
    """
    The list of fixtures to be loaded by the :manage:`initdb_demo`
    command.

    """

    use_spinner = False  # doesn't work. leave this to False

    #~ django_admin_prefix = '/django'
    django_admin_prefix = None
    """
    The prefix to use for Django admin URLs.
    Leave this unchanged as long as :srcref:`docs/tickets/70` is not solved.
    """

    time_format_extjs = 'H:i'
    """
    Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.

    """

    date_format_extjs = 'd.m.Y'
    """Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.

    """

    alt_date_formats_extjs = 'd/m/Y|Y-m-d'
    """Alternative date entry formats accepted by ExtJS Date widgets.

    """

    #~ default_number_format_extjs = '0,000.00/i'
    default_number_format_extjs = '0,00/i'

    uppercase_last_name = False
    """
    Whether last name of persons should (by default) be printed with
    uppercase letters.  See :mod:`lino.test_apps.human`

    """

    tinymce_base_url = "http://www.tinymce.com/js/tinymce/jscripts/tiny_mce/"
    "Replaced by :attr:`lino.modlib.tinymce.Plugin.media_base_url`."

    jasmine_root = None
    """Path to the Jasmine root directory.  Only used on a development
    server if the `media` directory has no symbolic link to the
    Jasmine root directory and only if :attr:`use_jasmine` is True.

    """

    # tinymce_root = None
    # "Replaced by :attr:`lino.modlib.tinymce.Plugin.media_root`."

    default_user = None
    """Username of the user to be used for all incoming requests.  Setting
    this to a nonempty value will disable authentication on this site.
    The special value `'anonymous'` will cause anonymous requests
    (whose `user` attribute is the :class:`AnonymousUser
    <lino.modlib.users.utils.AnonymousUser>` instance).

    See also :meth:`get_auth_method`.

    This setting should be `None` when :attr:`user_model` is `None`.

    """

    anonymous_user_profile = '000'
    """The user profile to be assigned to the anonymous user
(:class:`AnonymousUser <lino.modlib.users.utils.AnonymousUser>`).

    """

    remote_user_header = None
    """The name of the header (set by the web server) that Lino should
    consult for finding the user of a request.  The default value
    `None` means that http authentication is not used.  Apache's
    default value is ``"REMOTE_USER"``.

    """
    ldap_auth_server = None
    """
    This should be a string with the domain name and DNS (separated by a
    space) of the LDAP server to be used for authentication.  Example::

      ldap_auth_server = 'DOMAIN_NAME SERVER_DNS'

    """

    use_gridfilters = True

    use_eid_applet = False
    """Whether to include functionality to read Belgian id cards using
    the official `eid-applet <http://code.google.com/p/eid-applet>`_.
    This option is experimental and doesn't yet work.  See
    `/blog/2012/1105`.

    """

    use_esteid = False
    """
    Whether to include functionality to read Estonian id cards.
    This option is experimental and doesn't yet work.
    """

    use_filterRow = not use_gridfilters
    """
    See `/blog/2011/0630`.
    This option was experimental and doesn't yet work (and maybe never will).
    """

    use_awesome_uploader = False
    """
    Whether to use AwesomeUploader.
    This option was experimental and doesn't yet work (and maybe never will).
    """

    use_tinymce = True
    """Replaced by :mod:`lino.modlib.tinymce`.
    """

    use_jasmine = False
    """Whether to use the `Jasmine <https://github.com/pivotal/jasmine>`_
    testing library.

    """

    use_quicktips = True
    """Whether to make use of `Ext.QuickTips
    <http://docs.sencha.com/ext-js/3-4/#!/api/Ext.QuickTips>`_ for
    displaying :ref:`help_texts` and internal field names (if
    :attr:`show_internal_field_names`).

    """

    use_css_tooltips = False
    """
    Whether to make use of CSS tooltips
    when displaying help texts defined in :class:`lino.models.HelpText`.
    """

    use_vinylfox = False
    """
    Whether to use VinylFox extensions for HtmlEditor. 
    This feature was experimental and doesn't yet work (and maybe never will).
    See `/blog/2011/0523`.
    """

    webdav_root = None
    """
    The path on server to store webdav files.
    Default is :attr:`cache_dir` + ´/media/webdav'.
    """

    webdav_url = None
    """The URL prefix for webdav files.  In a normal production
    configuration you should leave this to `None`, Lino will set a
    default value "/media/webdav/", supposing that your Apache is
    configured as described in :doc:`/admin/webdav`.
    
    This may be used to simulate a :term:`WebDAV` location on a
    development server.  For example on a Windows machine, you may set
    it to ``w:\``, and before invoking :manage:`runserver`, you issue in
    a command prompt::
    
        subst w: <dev_project_path>\media\webdav

    """

    sidebar_width = 0
    """
    Used by :mod:`lino.modlib.plain`.
    Width of the sidebar in 1/12 of total screen width.
    Meaningful values are 0 (no sidebar), 2 or 3.

    """

    config_id = 1
    """The primary key of the one and only
    :class:`SiteConfig<lino.modlib.system.models.SiteConfig>` instance
    of this :class:`Site`. Default value is 1.

    This is Lino's equivalent of Django's :setting:`SITE_ID` setting.
    Lino applications don't need ``django.contrib.sites`` (`The "sites"
    framework
    <https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_) because
    this functionality is integral part of :mod:`lino.modlib.system`.

    """

    preview_limit = 15
    """Default value for the
    :attr:`preview_limit<lino.core.tables.AbstractTable.preview_limit>`
    parameter of all tables who don't specify their own one.  Default
    value is 15.

    """

    # default_ui = 'lino_extjs6.extjs6'
    default_ui = 'lino.modlib.extjs'
    """The full Python name of the plugin which is to be used as default
    user interface on this :class:`Site`.

    Default value is :mod:`lino.modlib.extjs`. Other candidates are
    :mod:`lino.modlib.bootstrap3`, :mod:`lino_xl.lib.pages` and
    :mod:`lino_extjs6.extjs6` .

    Another possibility is to set it to `None`. In that case you will
    probably also set :attr:`root_urlconf` to a custom URL dispatcher.
    Usage example for this see :mod:`lino.projects.cms`.

    """

    root_urlconf = 'lino.core.urls'
    """The value to be attribute to :setting:`ROOT_URLCONF` when this
    :class:`Site` instantiates.

    The default value is :mod:`lino.core.urls`.

    """

    textfield_format = 'plain'
    """The default format for text fields.
    Valid choices are currently 'plain' and 'html'.

    Text fields are either Django's `models.TextField` or
    :class:`lino.core.fields.RichTextField`.

    You'll probably better leave the global option as 'plain',
    and specify explicitly the fields you want as html by declaring
    them::

      foo = fields.RichTextField(...,format='html')

    We even recommend that you declare your *plain* text fields also
    using `fields.RichTextField` and not `models.TextField`::

      foo = fields.RichTextField()

    Because that gives subclasses of your application the possibility to
    make that specific field html-formatted::

       resolve_field('Bar.foo').set_format('html')

    """

    log_each_action_request = False
    """Whether Lino should log every incoming request for non
    :attr:`readonly <lino.core.actions.Action.readonly>` actions.

    This is experimental. Theoretically it is useless to ask Lino for
    logging every request since Apache does this. OTOH Lino can
    produce more readable logs.

    Note also that there is no warranty that actually *each* request
    is being logged.  It corrently works only for requests that are
    being processed by the kernel's :meth:`run_action
    <lino.core.kernel.Kernel.run_action>` or
    :meth:`run_callback
    <lino.core.kernel.Kernel.run_callback>` methods.

    """

    verbose_client_info_message = False
    """
    Set this to True if actions should send debug messages to the client.
    These will be shown in the client's Javascript console only.

    """

    help_url = "http://www.lino-framework.org"

    help_email = "users@lino-framework.org"
    """
    An e-mail address where users can get help. This is included in
    :xfile:`admin_main.html`.

    """

    catch_layout_exceptions = True
    """Lino usually catches any exception during startup (in
    :func:`create_layout_element
    <lino.core.layouts.create_layout_element>`) to report errors of
    style "Unknown element "postings.PostingsByController
    ('postings')" referred in layout <PageDetail on pages.Pages>."
    
    Setting this to `False` is useful when there's some problem
    *within* the framework.

    """

    strict_choicelist_values = True
    """Whether invalid values in a ChoiceList should raise an exception.

    This should be `True` except for exceptional situations.
    """

    csv_params = dict()
    """Site-wide default parameters for CSV generation.  This must be a
    dictionary that will be used as keyword parameters to Python
    `csv.writer()
    <http://docs.python.org/library/csv.html#csv.writer>`_
    
    Possible keys include:
    
    - encoding :
      the charset to use when responding to a CSV request.
      See
      http://docs.python.org/library/codecs.html#standard-encodings
      for a list of available values.
      
    - many more allowed keys are explained in
      `Dialects and Formatting Parameters
      <http://docs.python.org/library/csv.html#csv-fmt-params>`_.

    """

    logger_filename = 'system.log'
    """The name of Lino's main logger file, created in
    :meth:`setup_logging`.

    .. xfile:: system.log
    
        The default name of Lino's main logger file is
        :xfile:`system.log` for historical reasons.

        If you don't like that name, then replace it by something else
        and tell us how you named it. We are still discussing about a
        good successor. Candidates are :xfile:`main.log` and
        :xfile:`lino.log`.

    """
    auto_configure_logger_names = 'atelier lino'
    """
    A string with a space-separated list of logger names to be
    automatically configured. See :meth:`setup_logging`.

    """

    # appy_params = dict(ooPort=8100)
    appy_params = dict(
        ooPort=8100, pythonWithUnoPath='/usr/bin/python3',
        raiseOnError=True)
    """Used by :class:`lino.mixins.printable.AppyBuildMethod`.

    Allowed keyword arguments for `appy.pod.renderer.Render` are::

      pythonWithUnoPath=None,
      ooPort=2002
      stylesMapping={}
      forceOoCall=False,
      finalizeFunction=None
      overwriteExisting=False
      raiseOnError=False
      imageResolver=None

    See `the source code
    <http://bazaar.launchpad.net/~appy-dev/appy/trunk/view/head:/pod/renderer.py>`_
    for details.

    See also :doc:`/admin/oood`

    """

    #~ decimal_separator = '.'
    decimal_separator = ','
    """Set this to either ``'.'`` or ``','`` to define wether to use
    comma or dot as decimal point separator when entering a
    `DecimalField`.

    """

    # decimal_group_separator = ','
    # decimal_group_separator = ' '
    # decimal_group_separator = '.'
    decimal_group_separator = u"\u00A0"

    """
    Decimal group separator for :meth:`decfmt`.
    """

    time_format_strftime = '%H:%M'
    """
    Format (in strftime syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.

    """

    date_format_strftime = '%d.%m.%Y'
    """
    Format (in strftime syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.

    """

    date_format_regex = "/^[0123]?\d\.[01]?\d\.-?\d+$/"
    """
    Format (in Javascript regex syntax) to use for displaying dates to
    the user.  If you change this setting, you also need to override
    :meth:`parse_date`.

    """

    datetime_format_strftime = '%Y-%m-%dT%H:%M:%S'
    """
    Format (in strftime syntax) to use for formatting timestamps in
    AJAX responses.  If you change this setting, you also need to
    override :meth:`parse_datetime`.

    """

    datetime_format_extjs = 'Y-m-d\TH:i:s'
    """
    Format (in ExtJS syntax) to use for formatting timestamps in AJAX
    calls.  If you change this setting, you also need to override
    :meth:`parse_datetime`.

    """

    # for internal use:
    # _welcome_actors = []
    _welcome_handlers = []
    _site_config = None
    _logger = None
    override_modlib_models = None
    """A dictionary which maps model class names to the plugin which
    overrides them.

    This is automatically filled at startup.  You can inspect it, but
    you should not modify it.  Needed for :meth:`is_abstract_model`.

    The challenge is that we want to know exactly where every model's
    concrete class will be defined *before* actually starting to
    import the :xfile:`models.py` modules.  That's why we need
    :attr:`extends_models <lino.core.plugin.Plugin.extends_models>`.

    This can be tricky, see e.g. 20160205.

    """

    installed_plugin_modules = None
    """A set of the full Python paths of all imported plugin modules. Not
    just the plugin modules themselves but also those they inherit
    from. This is used internally by :meth:`is_abstract_model`.  Don't
    modify.

    """

    _help_texts = dict()

    def __init__(self, settings_globals=None, local_apps=[], **kwargs):
        """Every Lino application calls this once in it's
        :file:`settings.py` file.
        See :doc:`/usage`.

        `settings_globals` is the `globals()` dictionary of your
        :xfile:`settings.py`.

        """
        # self.logger.info("20140226 Site.__init__() a %s", self)
        #~ print "20130404 ok?"
        if 'no_local' in kwargs:
            kwargs.pop('no_local')
            # For the moment we just silently ignore it, but soon:
            if False:
                raise ChangedAPI("The no_local argument is no longer needed.")
        if settings_globals is None:
            settings_globals = {}
        self.init_before_local(settings_globals, local_apps)
        self.setup_logging()
        self.run_lino_site_module()
        self.override_settings(**kwargs)
        self.load_plugins()
        self.setup_plugins()
        self.install_settings()

        from lino.utils.config import ConfigDirCache
        self.confdirs = ConfigDirCache(self)

        for k in ('ignore_dates_before', 'ignore_dates_after'):
            if hasattr(self, k):
                msg = "{0} is no longer a site attribute"
                msg += " but a plugin attribute on lino_xl.lib.cal."
                msg = msg.format(k)
                raise ChangedAPI(msg)

        self.load_help_texts()

    def init_before_local(self, settings_globals, local_apps):
        """If your :attr:`project_dir` contains no :xfile:`models.py`, but
        *does* contain a `fixtures` subdir, then Lino automatically adds this
        as a local fixtures directory to Django's :setting:`FIXTURE_DIRS`.

        But only once: if your application defines its own local
        fixtures directory, then this directory "overrides" those of
        parent applications. E.g. lino_noi.projects.care does not want
        to load the application-specific fixtures of
        lino_noi.projects.team.

        """
        if isinstance(local_apps, six.string_types):
            local_apps = [local_apps]
        if not isinstance(settings_globals, dict):
            raise Exception("""
            The first argument when instantiating a %s
            must be your settings.py file's `globals()`
            and not %r
            """ % (self.__class__.__name__, settings_globals))

        if isinstance(local_apps, six.string_types):
            local_apps = [local_apps]
        self.local_apps = local_apps

        self.django_settings = settings_globals
        project_file = settings_globals.get('__file__', '.')

        self.project_dir = Path(dirname(project_file)).absolute().resolve()

        # inherit `project_name` from parent?
        # if self.__dict__.get('project_name') is None:
        if self.project_name is None:
            parts = reversed(self.project_dir.split(os.sep))
            # print(20150129, list(parts))
            for part in parts:
                if part != 'settings':
                    self.project_name = part
                    break

        cache_root = os.environ.get('LINO_CACHE_ROOT', None)
        if cache_root:
            cr = Path(cache_root).absolute()
            if not cr.exists():
                msg = "LINO_CACHE_ROOT ({0}) does not exist!".format(cr)
                raise Exception(msg)
            self.cache_dir = cr.child(self.project_name).resolve()
            self.setup_cache_directory()
        else:
            self.cache_dir = Path(self.project_dir).absolute()

        self._startup_done = False
        self.startup_time = datetime.datetime.now()

        db = self.get_database_settings()

        if db is not None:
            self.django_settings.update(DATABASES=db)

        self.update_settings(SERIALIZATION_MODULES={
            "py": "lino.utils.dpy",
        })

        if self.site_prefix != '/':
            if not self.site_prefix.endswith('/'):
                raise Exception("`site_prefix` must end with a '/'!")
            if not self.site_prefix.startswith('/'):
                raise Exception("`site_prefix` must start with a '/'!")
            self.update_settings(
                SESSION_COOKIE_PATH=self.site_prefix[:-1])
            # self.update_settings(SESSION_COOKIE_NAME='ssid')

        ## Local project directory
        modname = self.__module__
        i = modname.rfind('.')
        if i != -1:
            modname = modname[:i]
        self.is_local_project_dir = modname not in self.local_apps

        self.VIRTUAL_FIELDS = []

    def setup_logging(self):
        """Modifies the :data:`DEFAULT_LOGGING
        <django.utils.log.DEFAULT_LOGGING>` dictionary *before* Django
        passes it to the `logging.config.dictConfig
        <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`__
        function.

        It is designed to work with the :setting:`LOGGING` and
        :setting:`LOGGER_CONFIG` settings unmodified.

        It does the following modifications:

        - Define a *default logger configuration* which is initially
          the same as the one used by Django::

            {
                'handlers': ['console', 'mail_admins'],
                'level': 'INFO',
            }

        - If the :attr:`project_dir` has a subdirectory named ``log``,
          and if :attr:`logger_filename` is not empty, add a handler
          named ``file`` and a formatter named ``verbose``, and add
          that handler to the default logger configuration.

        - Apply the default logger configuration to every logger name
          in :attr:`auto_configure_logger_names`.

        It does nothing at all if :attr:`auto_configure_logger_names`
        is set to `None` or empty.

        See also Django's doc about `Logging
        <https://docs.djangoproject.com/en/1.9/topics/logging/>`__.

        """
        if not self.auto_configure_logger_names:
            return

        from django.utils.log import DEFAULT_LOGGING
        d = DEFAULT_LOGGING

        loggercfg = {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        }

        handlers = d.setdefault('handlers', {})
        if self.logger_filename and 'file' not in handlers:
            logdir = self.project_dir.child('log')
            if logdir.isdir():
                formatters = d.setdefault('formatters', {})
                formatters.setdefault('verbose', dict(
                    format='%(asctime)s %(levelname)s '
                    '%(module)s : %(message)s',
                    datefmt='%Y%m-%d %H:%M:%S'))
                handlers['file'] = {
                    'level': 'INFO',
                    'class': 'logging.FileHandler',
                    'filename': logdir.child(self.logger_filename),
                    'encoding': 'UTF-8',
                    'formatter': 'verbose',
                }
                loggercfg['handlers'].append('file')

        for name in self.auto_configure_logger_names.split():
            # if name not in d['loggers']:
            d['loggers'][name] = loggercfg

        # self.update_settings(LOGGING=d)
        # from pprint import pprint
        # pprint(d)
        # import yaml
        # print(yaml.dump(d))

    def get_database_settings(self):
        """Return a dict to be set as the :setting:`DATABASE` setting.
        
        The default behaviour uses SQLiite on a file named
        :xfile:`default.db` in the :attr:`cache_dir`, and in
        ``:memory:`` when :attr:`cache_dir` is `None`.

        And alternative might be for example::

            def get_database_settings(self):
                return {
                    'default': {
                        'ENGINE': 'django.db.backends.mysql',
                        'NAME': 'test_' + self.project_name,
                        'USER': 'django',
                        'PASSWORD': os.environ['MYSQL_PASSWORD'],
                        'HOST': 'localhost',                  
                        'PORT': 3306,
                        'OPTIONS': {
                           "init_command": "SET storage_engine=MyISAM",
                        }
                    }
                }

        

        """
        if self.cache_dir is None:
            pass  # raise Exception("20160516 No cache_dir")
        else:
            dbname = self.cache_dir.child('default.db')
            return {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': dbname
                }
            }

    def run_lino_site_module(self):
        """See :ref:`djangosite_local`.

        """
        site_module = os.environ.get('LINO_SITE_MODULE', None)
        if site_module:
            mod = import_module(site_module)
            func = getattr(mod, 'setup_site', None)
            if func:
                func(self)
        # try:
        #     from djangosite_local import setup_site
        # except ImportError:
        #     pass
        # else:
        #     setup_site(self)

    def override_settings(self, **kwargs):
        # Called internally during `__init__` method.
        # Also called from :mod:`lino.utils.djangotest`

        #~ logger.info("20130404 lino.site.Site.override_defaults")

        for k, v in list(kwargs.items()):
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self.__class__, k))
            setattr(self, k, v)

        self.apply_languages()

    def load_plugins(self):
        """Load all plugins and build the :setting:`INSTALLED_APPS` setting
        for Django.

        This includes a call to :meth:`get_apps_modifiers` and
        :meth:`get_installed_apps`.

        """
        # Called internally during `__init__` method.

        requested_apps = []
        apps_modifiers = self.get_apps_modifiers()

        if hasattr(self, 'hidden_apps'):
            raise ChangedAPI("Replace hidden_apps by get_apps_modifiers()")

        def add(x):
            if isinstance(x, six.string_types):
                app_label = x.split('.')[-1]
                x = apps_modifiers.pop(app_label, x)
                if x:
                    requested_apps.append(x)
            else:
                # if it's not a string, then it's an iterable of strings
                for xi in x:
                    add(xi)

        for x in self.get_installed_apps():
            add(x)

        # actual_apps = []
        plugins = []
        disabled_plugins = set()
        self.plugins = AttrDict()

        def install_plugin(app_name, needed_by=None):
            # Django does not accept newstr, and we don't want to see
            # ``u'applabel'`` in doctests.
            app_name = six.text_type(app_name)
            # print("20160524 install_plugin(%r)" % app_name)
            app_mod = import_module(app_name)

            # print "Loading plugin", app_name
            k = app_name.rsplit('.')[-1]
            x = apps_modifiers.pop(k, 42)
            if x is None:
                return
            elif x == 42:
                pass
            else:
                raise Exception("20160712")
            if k in self.plugins:
                other = self.plugins[k]
                if other.app_name == app_name:
                    # If a plugin is installed more than once, only
                    # the first one counts and all others are ignored
                    # silently. Happens e.g. in Lino Noi where
                    # lino_noi.lib.noi is both a required plugin and
                    # the default_ui.
                    return
                raise Exception("Tried to install %r where %r "
                                "is already installed." % (
                                    app_name, other.app_name))

            # Can an `__init__.py` file explicitly set ``Plugin =
            # None``? Is that feature being used?
            app_class = getattr(app_mod, 'Plugin', None)
            if app_class is None:
                app_class = Plugin
            p = app_class(self, k, app_name, app_mod, needed_by)
            cfg = PLUGIN_CONFIGS.pop(k, None)
            if cfg:
                p.configure(**cfg)

            for dep in p.needs_plugins:
                k2 = dep.rsplit('.')[-1]
                if k2 not in self.plugins:
                    install_plugin(dep, needed_by=p)
                    # plugins.append(dep)

            # actual_apps.append(app_name)
            plugins.append(p)
            self.plugins.define(k, p)
            for dp in p.disables_plugins:
                disabled_plugins.add(dp)

        # lino_startup is always the first plugin:
        install_plugin(str('lino.modlib.lino_startup'))

        for app_name in requested_apps:
            install_plugin(app_name)

        if apps_modifiers:
            raise Exception(
                "Invalid app_label '{0}' in your get_apps_modifiers!".format(
                    list(apps_modifiers.keys())[0]))

        # The return value of get_auth_method() may depend on a
        # plugin, so if needed we must add the django.contrib.sessions
        # afterwards.
        if self.get_auth_method() == 'session':
            # actual_apps.insert(0, str('django.contrib.sessions'))
            install_plugin(str('django.contrib.sessions'))

        # install_plugin(str('lino.modlib.database_ready'))

        for p in plugins:
            if p.app_label in disabled_plugins \
               or p.app_name in disabled_plugins:
                plugins.remove(p)
                del self.plugins[p.app_label]

        # self.update_settings(INSTALLED_APPS=tuple(actual_apps))
        self.update_settings(
            INSTALLED_APPS=tuple([p.app_name for p in plugins]))
        self.installed_plugins = tuple(plugins)

        if self.override_modlib_models is not None:
            raise ChangedAPI("override_modlib_models no longer allowed")

        self.override_modlib_models = dict()

        # def reg(p, pp, m):
        #     name = pp.__module__ + '.' + m
        #     self.override_modlib_models[name] = p

        def plugin_parents(pc):
            for pp in pc.__mro__:
                if issubclass(pp, Plugin):
                    # if pp not in (Plugin, p.__class__):
                    if pp is not Plugin:
                        yield pp

        def reg(pc):
            # If plugin p extends some models, then tell all parent
            # plugins to make their definition of each model abstract.
            extends_models = pc.__dict__.get('extends_models')
            if extends_models is not None:
                for m in extends_models:
                    if "." in m:
                        raise Exception(
                            "extends_models in %s still uses '.'" % pc)
                    for pp in plugin_parents(pc):
                        if pp is pc:
                            continue
                        name = pp.__module__ + '.' + m
                        self.override_modlib_models[name] = pc
                        # if m == "Company":
                        #     print("20160524 tell %s that %s extends %s" % (
                        #         pp, p.app_name, m))

            for pp in plugin_parents(pc):
                if pp is pc:
                    continue
                reg(pp)


            # msg = "{0} declares to extend_models {1}, but " \
            #       "cannot find parent plugin".format(p, m)
            # raise Exception(msg)

        for p in self.installed_plugins:
            reg(p.__class__)
            # for pp in plugin_parents(p.__class__):
            #     if p.app_label == 'contacts':
            #         print("20160524c %s" % pp)
            #     reg(p.__class__)

        # for m, p in self.override_modlib_models.items():
        #     print("20160524 %s : %s" % (m, p))

        self.installed_plugin_modules = set()
        for p in self.installed_plugins:
            # self.installed_plugin_modules.add(p.__module__)
            for pp in plugin_parents(p.__class__):
                self.installed_plugin_modules.add(pp.__module__)

        # print("20160524 %s", self.installed_plugin_modules)
                        
        # raise Exception("20140825 %s", self.override_modlib_models)

        # Tried to prevent accidental calls to configure_plugin()
        # *after* Site initialization.

        # global PLUGIN_CONFIGS
        # PLUGIN_CONFIGS = None

    def load_help_texts(self):
        """Collect :xfile:`help_texts.py` files"""
        for p in self.installed_plugins:
            mn = p.app_name + '.help_texts'
            try:
                m = import_module(mn)
                self._help_texts.update(m.help_texts)
            except ImportError:
                pass

    def install_help_text(self, fld, attrname):
        """Install a `help_text` from collected :xfile:`help_texts.py` for
this field.

        """
        if not hasattr(fld, 'help_text'):  # some fields don't have
            return
        if fld.help_text:
            # print("20160620 {} has already a help_text".format(fld))
            return
        for m in fld.model.mro():
            k = m.__module__ + '.' + m.__name__
            if attrname:
                k += '.' + attrname
            txt = self._help_texts.get(k, None)
            if txt is None:
                pass
                # print("20160620 {} no help_text found using {}".format(fld, k))
            else:
                # print("20160620 {} help_text found using {}".format(fld, k))
                fld.help_text = txt
                return

    def setup_plugins(self):
        """This method is called exactly once during site startup, after
        :meth:`load_plugins` but before populating the models
        registry.

        """
        pass

    def install_settings(self):

        assert not self.help_url.endswith('/')
        # import django
        # django.setup()
        if self.cache_dir is not None:
            if self.webdav_url is None:
                self.webdav_url = self.site_prefix + 'media/webdav/'
            if self.webdav_root is None:
                self.webdav_root = join(self.cache_dir, 'media', 'webdav')
            self.django_settings.update(
                MEDIA_ROOT=join(self.cache_dir, 'media'))

        self.update_settings(ROOT_URLCONF=self.root_urlconf)
        self.update_settings(MEDIA_URL='/media/')

        if not self.django_settings.get('STATIC_ROOT', False):
            cache_root = os.environ.get('LINO_CACHE_ROOT', None)
            if cache_root:
                self.django_settings.update(
                    STATIC_ROOT=Path(cache_root).child('collectstatic'))
            else:
                self.django_settings.update(
                    STATIC_ROOT=self.cache_dir.child('static'))
        if not self.django_settings.get('STATIC_URL', False):
            self.update_settings(STATIC_URL='/static/')

        loaders = [
            'lino.modlib.jinja.loader.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            #~ 'django.template.loaders.eggs.Loader',
        ]

        tcp = []
        if self.user_model == 'auth.User':  # not tested
            self.update_settings(LOGIN_URL='/accounts/login/')
            self.update_settings(LOGIN_REDIRECT_URL="/")
            tcp += ['django.contrib.auth.context_processors.auth']

        tcp += [
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
        ]
        # self.update_settings(TEMPLATE_LOADERS=tuple(loaders))
        # self.update_settings(TEMPLATE_CONTEXT_PROCESSORS=tuple(tcp))

        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': tcp,
                    # 'loaders': loaders
                },
            },
        ]
        TEMPLATES.append(
            {
                'BACKEND': 'django.template.backends.jinja2.Jinja2',
                'DIRS': [],
                'OPTIONS': {
                    'environment': 'lino.modlib.jinja.get_environment'
                },
            })

        self.update_settings(TEMPLATES=TEMPLATES)

        self.define_settings(
            MIDDLEWARE_CLASSES=tuple(self.get_middleware_classes()))

        def collect_settings_subdirs(lst, name, max_count=None):
            def add(p):
                p = p.replace(os.sep, "/")
                if p not in lst:
                    lst.append(p)

            for p in self.get_settings_subdirs(name):
                # if the parent of a settings subdir has a
                # `models.py`, then it is a plugin and we must not add
                # the subdir because Django does that.
                if exists(join(p, '..', 'models.py')):
                    self.logger.info(
                        "Ignoring %s %s because it is a plugin", p, name)
                else:
                    add(p)
                    if (max_count is not None) and len(lst) >= max_count:
                        break

            # local_dir = self.cache_dir.child(name)
            # if local_dir.exists():
            #     print "20150427 adding local directory %s" % local_dir
            #     add(local_dir)
            # The STATICFILES_DIRS setting should not contain the
            # STATIC_ROOT setting

            if False:
                # If a plugin has no "fixtures" ("config") directory
                # of its own, inherit it from parents.  That would be
                # nice and it even works, but with a stud: these
                # fixtures will be loaded at the end.
                for ip in self.installed_plugins:
                    if not ip.get_subdir(name):
                        pc = ip.extends_from()
                        while pc and issubclass(pc, Plugin):
                            p = pc.get_subdir(name)
                            if p:
                                add(p)
                            pc = pc.extends_from()

        fixture_dirs = list(self.django_settings.get('FIXTURE_DIRS', []))
        locale_paths = list(self.django_settings.get('LOCALE_PATHS', []))
        sfd = list(self.django_settings.get('STATICFILES_DIRS', []))
        # sfd.append(self.cache_dir.child('genjs'))
        collect_settings_subdirs(fixture_dirs, 'fixtures', 1)
        collect_settings_subdirs(locale_paths, 'locale')
        collect_settings_subdirs(sfd, 'static')
        self.update_settings(FIXTURE_DIRS=tuple(fixture_dirs))
        self.update_settings(LOCALE_PATHS=tuple(locale_paths))
        self.update_settings(STATICFILES_DIRS=tuple(sfd))

        # print(20150331, self.django_settings['FIXTURE_DIRS'])

    def setup_cache_directory(self):
        """When :envvar:`LINO_CACHE_ROOT` is set, Lino adds a stamp file
        called :xfile:`lino_cache.txt` to every project's cache
        directory in order to avoid duplicate use of same cache
        directory.

        .. xfile:: lino_cache.txt

            A small text file with one line of text which contains the
            path of the project which uses this cache directory.

        """

        stamp = self.cache_dir.child('lino_cache.txt')
        this = class2str(self.__class__)
        if stamp.exists():
            other = stamp.read_file()
            if other == this:
                ok = True
            else:
                ok = False
                for parent in self.__class__.__mro__:
                    if other == class2str(parent):
                        ok = True
                        break
            if not ok:
                # Can happen e.g. when `python -m lino.hello` is
                # called.  in certain conditions.
                msg = ("Cannot use {cache_dir} for {this} "
                       "because it is used for {other}. (Settings {settings})")
                msg = msg.format(
                    cache_dir=self.cache_dir,
                    this=this,
                    settings=self.django_settings.get('SETTINGS_MODULE'),
                    other=other)
                if True:
                    raise Exception(msg)
                else:
                    # print(msg)
                    self.cache_dir = None
        else:
            self.makedirs_if_missing(self.cache_dir)
            stamp.write_file(this)

    def set_user_model(self, spec):
        """This can be called during the :meth:`on_init
        <lino.core.plugin.Plugin.on_init>` of plugins which provide
        user management (the only plugin which does this is currently
        :mod:`lino.modlib.users`).

        """
        if self.user_model is not None:
            msg = "Site.user_model was already set!"
            # Theoretically this should raise an exception. But in a
            # transitional phase after 20150116 we just ignore it. A
            # warning would be nice, but we cannot use the logger here
            # since it is not yet configured.
            if False:
                # self.logger.warning(msg)
                raise Exception(msg)
        self.user_model = spec

    def get_auth_method(self):
        """Returns the authentication method used on this site. This is one of
        `None`, `'remote'` or `'session'`.

        It depends on the values in
        :attr:`user_model`,
        :attr:`default_user` and
        :attr:`remote_user_header`.

        It influences the results of
        :meth:`get_middleware_classes` and
        :meth:`get_installed_apps`.

        """
        if self.user_model is None:
            return None
        if self.default_user is not None:
            return None
        if self.remote_user_header is None:
            return 'session'
        return 'remote'

    def get_apps_modifiers(self, **kw):
        """Override or hide individual plugins of an existing application.

        For example, if your site inherits from
        :mod:`lino.projects.min2`::

            def get_apps_modifiers(self, **kw):
                kw.update(sales=None)
                kw.update(courses='my.modlib.courses')
                return kw

        The default implementation returns an empty dict.

        This method adds an additional level of customization because
        it lets you remove or replace individual plugins from
        :setting:`INSTALLED_APPS` without rewriting your own
        :meth:`get_installed_apps`.

        This will be called during Site instantiation and is expected to
        return a dict of `app_label` to `full_python_path`
        mappings which you want to override in the list of plugins
        returned by :meth:`get_installed_apps`.

        Mapping an `app_label` to `None` will remove that plugin from
        :setting:`INSTALLED_APPS`.

        It is theoretically possible but not recommended to replace an
        existing `app_label` by an app with a different
        `app_label`. For example, the following might work but is not
        recommended::

                kw.update(courses='my.modlib.mycourses')

        """

        return kw

    def is_hidden_app(self, app_label):
        """
        Return True if the app is known, but has been disabled using
        :meth:`get_apps_modifiers`.

        """
        am = self.get_apps_modifiers()
        if am.get(app_label, 1) is None:
            return True

    def update_settings(self, **kw):
        """This may be called from within a :doc:`djangosite_local.setup_site
        </admin/djangosite_local>` function.

        """
        self.django_settings.update(**kw)

    def define_settings(self, **kwargs):
        """Same as :meth:`update_settings`, but raises an exception if a
        setting already exists.
        
        TODO: Currently this exception is deactivated.  Because it
        doesn't work as expected.  For some reason (maybe because
        settings is being imported twice on a devserver) it raises a
        false exception when :meth:`override_defaults` tries to use it
        on `MIDDLEWARE_CLASSES`...

        """
        if False:
            for name in list(kwargs.keys()):
                if name in self.django_settings:
                    raise Exception(
                        "Tried to define existing Django setting %s" % name)
        self.django_settings.update(kwargs)

    _starting_up = False

    def startup(self):
        """Start up this Site.

        You probably don't want to override this method since it is
        designed to be called potentially several times in case your
        code wants to make sure that it was called.

        This is called exactly once when Django has has populated it's model
        cache.

        """

        # This code can run several times at once when running
        # e.g. under mod_wsgi: another thread has started and not yet
        # finished `startup()`.

        with startup_rlock:

            # if self.cache_dir is not None:
            #     raise Exception("No cache_dir is defined. "
            #                     "Check your LINO_CACHE_ROOT and project_name.")

            if self._starting_up:
                # This is needed because Django "somehow" imports the
                # settings module twice. The phenomen is not fully
                # explained, but without this test we had the startup
                # code being run twice, which caused various error
                # messages (e.g. Duplicate label in workflow setup)
                return

            if self._startup_done:
                # self.logger.info("20140227 Lino startup already done")
                return

            self._starting_up = True

            # print "20151010 Site.startup()"

            # if AFTER17:
            #     print "20151010 Site.startup() gonna call django.setup"
            #     import django
            #     django.setup()

            from lino.core.signals import pre_startup, post_startup

            pre_startup.send(self)
            # lino_startup = False
            # for index , plugin in enumerate(self.installed_plugins):
            #     if 'lino_startup' in plugin.app_name:
            #         lino_startup = plugin
            #         del plugin

            # if lino_startup:
            #     badguy = list(self.installed_plugins)
            #     badguy.append(lino_startup)
            #     # badguy = tuple(badguy)
            #     self.installed_plugins = tuple(badguy)

            # from django.conf import settings
            # import django
            #
            # if not settings.INSTALLED_APPS:
            #     django.setup()

            for p in self.installed_plugins:
                # m = loading.load_app(p.app_name, False)
                if AFTER17:
                    # In Django17+ we cannot say can_postpone=False,
                    # and we don't need to, because anyway we used it
                    # just for our hack in `lino.models`
                    # load_app(app_name) is deprecated
                    # from django.apps import apps
                    # m = apps.load_app(p.app_name)
                    try:
                        from django.apps import apps
                        app_config = AppConfig.create(p.app_name)
                        app_config.import_models(
                            apps.all_models[app_config.label])
                        apps.app_configs[app_config.label] = app_config
                        apps.clear_cache()
                        m = app_config.models_module
                    except ImportError:
                        self.logger.debug("No module {0}.models", p.app_name)
                        # print(rrrr)
                else:
                    from django.db.models import loading
                    m = loading.load_app(p.app_name, False)

                self.models.define(six.text_type(p.app_label), m)

            for p in self.installed_plugins:
                p.on_site_startup(self)
            self.do_site_startup()
            # self.logger.info("20140227 Site.do_site_startup() done")
            post_startup.send(self)

            self._startup_done = True

    @property
    def logger(self):
        if self._logger is None:
            import logging
            self._logger = logging.getLogger(__name__)
        return self._logger

    def get_settings_subdirs(self, subdir_name):
        """Yield all (existing) directories named `subdir_name` of this Site's
        project directory and it's inherited project directories.

        """
        # if local settings.py doesn't subclass Site:
        if self.project_dir != normpath(dirname(
                inspect.getfile(self.__class__))):
            pth = join(self.project_dir, subdir_name)
            if isdir(pth):
                yield pth

        for cl in self.__class__.__mro__:
            #~ logger.info("20130109 inspecting class %s",cl)
            if cl is not object and not inspect.isbuiltin(cl):
                pth = join(dirname(inspect.getfile(cl)), subdir_name)
                if isdir(pth):
                    yield pth

    def makedirs_if_missing(self, dirname):
        """Make missing directories if they don't exist and if
        :attr:`make_missing_dirs` is `True`.

        """
        if dirname and not isdir(dirname):
            if self.make_missing_dirs:
                os.makedirs(dirname)
            else:
                raise Exception("Please create yourself directory %s" %
                                dirname)

    def is_abstract_model(self, module_name, model_name):
        """Return True if the named model is declared as being extended by
        :attr:`lino.core.plugin.Plugin.extends_models`.

        Typical usage::

            class MyModel(dd.Model):
                 class Meta:
                     abstract = dd.is_abstract_model(__name__, 'MyModel')

        See :doc:`/dev/plugin_inheritance`.

        """
        app_name = '.'.join(module_name.split('.')[:-1])
        model_name = app_name + '.' + model_name
        rv = model_name in self.override_modlib_models
        if not rv:
            if app_name not in self.installed_plugin_modules:
                return True
        # if model_name.endswith('Company'):
        #     self.logger.info(
        #         "20160524 is_abstract_model(%s) -> %s", model_name, rv)
            # self.logger.info(
            #     "20160524 is_abstract_model(%s) -> %s (%s, %s)",
            #     model_name, rv, self.override_modlib_models.keys(),
            #     os.getenv('DJANGO_SETTINGS_MODULE'))
        return rv

    def is_installed_model_spec(self, model_spec):
        """Deprecated. This feature was a bit too automagic and caused bugs
        to pass silently.  See e.g. :blogref:`20131025`.

        """
        if False:  # mod_wsgi interprets them as error
            warnings.warn("is_installed_model_spec is deprecated.",
                          category=DeprecationWarning)

        if model_spec == 'self':
            return True
        app_label, model_name = model_spec.split(".")
        return self.is_installed(app_label)

    def is_installed(self, app_label):
        """
        Return `True` if :setting:`INSTALLED_APPS` contains an item
        which ends with the specified `app_label`.

        """
        return app_label in self.plugins

    def setup_model_spec(self, obj, name):
        """If the value of the named attribute of `obj` is a string, replace
        it by the model specified by that string.

        Example usage::

            # library code:
            class ThingBase(object):
                the_model = None

                def __init__(self):
                    settings.SITE.setup_model_spec(self, 'the_model')
    
            # user code:
            class MyThing(ThingBase):
                the_model = "contacts.Partner"


        """
        spec = getattr(obj, name)
        if spec and isinstance(spec, six.string_types):
            if not self.is_installed_model_spec(spec):
                setattr(obj, name, None)
                return
            from lino.core.utils import resolve_model
            msg = "Unresolved model '%s' in {0}.".format(name)
            setattr(obj, name, resolve_model(spec, strict=msg))

    def on_each_app(self, methname, *args):
        """Call the named method on the :xfile:`models.py` module of each
        installed app.

        Note that this mechanism is deprecated. It is still used (on
        names like ``setup_workflows`` and ``setup_site``) for
        historical reasons but will disappear one day.

        """
        if AFTER17:
            from django.apps import apps
            apps = [a.models_module for a in apps.get_app_configs()]
        else:
            from django.db.models import loading
            apps = loading.get_apps()
        for mod in apps:
            meth = getattr(mod, methname, None)
            if meth is not None:
                if False:  # 20150925 once we will do it for good...
                    raise ChangedAPI("{0} still has a function {1}".format(
                        mod, methname))
                meth(self, *args)

    def for_each_app(self, func, *args, **kw):
        """
        Call the given function on each installed app.
        Successor of :meth:`on_each_app`.  This also loops over

        - apps that don't have a models module
        - inherited apps

        """

        from importlib import import_module
        done = set()
        for p in self.installed_plugins:
            for b in p.__class__.__mro__:
                if b not in (object, Plugin):
                    if b.__module__ not in done:
                        done.add(b.__module__)
                        parent = import_module(b.__module__)
                        func(b.__module__, parent, *args, **kw)
            if p.app_name not in done:
                func(p.app_name, p.app_module, *args, **kw)

    def demo_date(self, *args, **kwargs):
        """
        Deprecated. Should be replaced by :meth:`today`.
        Compute a date using :func:`atelier.utils.date_offset` based on
        the process startup time (or :attr:`the_demo_date` if this is
        set).

        Used in Python fixtures and unit tests.


        """
        base = self.the_demo_date or self.startup_time.date()
        return date_offset(base, *args, **kwargs)

    def today(self, *args, **kwargs):
        """This is almost equivalent to calling :func:`datetime.date.today`.

        The difference is when :attr:`the_demo_date` is set, in which
        case :meth:`today` will return that date.

        Another difference is that any arguments are forwarded to
        :func:`atelier.utils.date_offset`.

        This feature is being used in many test cases where e.g. the
        age of people would otherwise change.

        """
        if self.site_config is not None:
            base = self.site_config.simulate_today \
                or self.the_demo_date or datetime.date.today()
        else:
            base = self.the_demo_date or datetime.date.today()
        return date_offset(base, *args, **kwargs)

    def welcome_text(self):
        """Returns the text to display in a console window when this Site
        starts.

        """
        return "This is %s using %s." % (
            self.site_version(), self.using_text())

    def using_text(self):
        """
        Text to display in a console window when Lino starts.
        """
        return ', '.join([u"%s %s" % (n, v)
                          for n, v, u in self.get_used_libs()])

    def site_version(self):
        """Used in footnote or header of certain printed documents.

        """
        if self.version:
            return self.verbose_name + ' ' + self.version
        return self.verbose_name

    def configure_plugin(self, app_label, **kw):
        raise Exception("Replace SITE.configure_plugin by ad.configure_plugin")

    def install_migrations(self, *args):
        """
        See :func:`lino.utils.dpy.install_migrations`.
        """
        from lino.utils.dpy import install_migrations
        install_migrations(self, *args)

    def parse_date(self, s):
        """Convert a string formatted using :attr:`date_format_strftime` or
        :attr:`date_format_extjs` into a `(y,m,d)` tuple (not a
        `datetime.date` instance).  See `/blog/2010/1130`.

        """
        ymd = tuple(reversed(list(map(int, s.split('.')))))
        assert len(ymd) == 3
        return ymd
        #~ return datetime.date(*ymd)

    def parse_time(self, s):
        """Convert a string formatted using :attr:`time_format_strftime` or
        :attr:`time_format_extjs` into a `datetime.time` instance.

        """
        hms = list(map(int, s.split(':')))
        return datetime.time(*hms)

    def parse_datetime(self, s):
        """Convert a string formatted using :attr:`datetime_format_strftime`
        or :attr:`datetime_format_extjs` into a `datetime.datetime`
        instance.

        """
        #~ print "20110701 parse_datetime(%r)" % s
        #~ s2 = s.split()
        s2 = s.split('T')
        if len(s2) != 2:
            raise Exception("Invalid datetime string %r" % s)
        ymd = list(map(int, s2[0].split('-')))
        hms = list(map(int, s2[1].split(':')))
        return datetime.datetime(*(ymd + hms))
        #~ d = datetime.date(*self.parse_date(s[0]))
        #~ return datetime.combine(d,t)

    def strftime(self, t):
        if t is None:
            return ''
        return t.strftime(self.time_format_strftime)

    def resolve_virtual_fields(self):
        for vf in self.VIRTUAL_FIELDS:
            vf.lino_resolve_type()
        self.VIRTUAL_FIELDS = []

    def register_virtual_field(self, vf):
        self.VIRTUAL_FIELDS.append(vf)

    def do_site_startup(self):
        """This method is called exactly once during site startup,
        just between the pre_startup and the post_startup signals.
        A hook for subclasses.

        TODO: rename this to `on_startup`?

        If you override it, don't forget to call the super method
        which calls :meth:`on_site_startup
        <lino.core.plugin.Plugin.on_site_startup>` for each installed
        plugin.

        """
        # self.logger.info("20160526 %s do_site_startup() a", self.__class__)

        self.user_interfaces = tuple([
            p for p in self.installed_plugins if p.ui_label is not None])

        # self.logger.info("20150428 user_interfaces %s", self.user_interfaces)

        from lino.core.kernel import Kernel
        self.kernel = Kernel(self)
        self.kernel.kernel_startup(self)
        # self.ui = self.kernel  # internal backwards compat

        # self.logger.info("20160526 %s do_site_startup() b", self.__class__)

    def find_config_file(self, *args, **kwargs):
        return self.confdirs.find_config_file(*args, **kwargs)

    def find_template_config_files(self, *args, **kwargs):
        return self.confdirs.find_template_config_files(*args, **kwargs)

    def setup_user_profiles(self):
        """Deprecated. Use :attr:`user_profiles_module` instead.

        """
        pass

    def setup_choicelists(self):
        """This is a hook for code to be run *after* all plugins have been
        instantiated and *before* the models are being discovered.

        This is useful for redefining your application's ChoiceLists.

        Note that you may not specify values longer than `max_length` when
        redefining your choicelists.  This limitation is because these
        redefinitions happen at a moment where database fields have
        already been instantiated, so it is too late to change their
        max_length.  Note that this limitation is only for the *values*,
        not for the names or texts of choices.

        """
        self.setup_user_profiles()

    # def setup_workflows(self):
    #     """Deprecated. Define a :attr:`workflows_module` instead.
    #     """
    #     self.on_each_app('setup_workflows')

    def setup_actions(self):
        """Hook for subclasses to add or modify actions.

        Usage example::

            def setup_actions(self):
                super(Site, self).setup_actions()
                from lino.core.merge import MergeAction
                partners = self.models.contacts
                for m in (partners.Person, partners.Organisation):
                    m.define_action(merge_row=MergeAction(m))

        """
        pass

    def setup_layouts(self):
        '''Hook for subclasses to add or modify layouts.
        
        Usage example::

            def setup_layouts(self):
                super(Site, self).setup_layouts()

                self.models.system.SiteConfigs.set_detail_layout("""
                site_company next_partner_id:10
                default_build_method
                clients_account   sales_account     sales_vat_account
                suppliers_account purchases_account purchases_vat_account
                """)

                self.models.accounts.Accounts.set_detail_layout("""
                ref:10 name id:5
                seqno group type clearable
                ledger.MovementsByAccount
                """)

        '''
        pass

    def add_user_field(self, name, fld):
        if self.user_model:
            from lino.api import dd
            dd.inject_field(self.user_model, name, fld)

    def get_used_libs(self, html=None):
        """
        Yield a list of (name, version, url) tuples describing the
        third-party software used on this Site.

        This function is used by :meth:`using_text` which is used by
        :meth:`welcome_text`.

        """

        import lino
        yield ("Lino", lino.SETUP_INFO['version'], lino.SETUP_INFO['url'])

        try:
            import mod_wsgi
            version = "{0}.{1}".format(*mod_wsgi.version)
            yield ("mod_wsgi", version, "http://www.modwsgi.org/")
        except ImportError:
            pass

        import django
        yield ("Django", django.get_version(), "http://www.djangoproject.com")

        import sys
        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python", version, "http://www.python.org/")

        import babel
        yield ("Babel", babel.__version__, "http://babel.edgewall.org/")

        #~ import tidylib
        #~ version = getattr(tidylib,'__version__','')
        #~ yield ("tidylib",version,"http://countergram.com/open-source/pytidylib")

        #~ import pyPdf
        #~ version = getattr(pyPdf,'__version__','')
        #~ yield ("pyPdf",version,"http://countergram.com/open-source/pytidylib")

        import jinja2
        version = getattr(jinja2, '__version__', '')
        yield ("Jinja", version, "http://jinja.pocoo.org/")

        import sphinx
        version = getattr(sphinx, '__version__', '')
        yield ("Sphinx", version, "http://sphinx-doc.org/")

        import dateutil
        version = getattr(dateutil, '__version__', '')
        yield ("python-dateutil", version, "http://labix.org/python-dateutil")

        #~ try:
            #~ import Cheetah
            #~ version = Cheetah.Version
            #~ yield ("Cheetah",version ,"http://cheetahtemplate.org/")
        #~ except ImportError:
            #~ pass

        try:
            from odf import opendocument
            version = opendocument.__version__
        except ImportError:
            version = self.not_found_msg
        yield ("OdfPy", version, "http://pypi.python.org/pypi/odfpy")

        try:
            import docutils
            version = docutils.__version__
        except ImportError:
            version = self.not_found_msg
        yield ("docutils", version, "http://docutils.sourceforge.net/")

        try:
            import suds
            version = suds.__version__
        except ImportError:
            version = self.not_found_msg
        yield ("suds", version, "https://fedorahosted.org/suds/")

        import yaml
        version = getattr(yaml, '__version__', '')
        yield ("PyYaml", version, "http://pyyaml.org/")

        if False:
            try:
                import pyratemp
                version = getattr(pyratemp, '__version__', '')
            except ImportError:
                version = self.not_found_msg
            yield ("pyratemp", version,
                   "http://www.simple-is-better.org/template/pyratemp.html")

        if False:
            try:
                import ho.pisa as pisa
                version = getattr(pisa, '__version__', '')
                yield ("xhtml2pdf", version, "http://www.xhtml2pdf.com")
            except ImportError:
                pass

            try:
                import reportlab
                version = reportlab.Version
            except ImportError:
                version = self.not_found_msg
            yield ("ReportLab", version,
                   "http://www.reportlab.org/rl_toolkit.html")

        try:
            #~ import appy
            from appy import version
            version = version.verbose
        except ImportError:
            version = self.not_found_msg
        yield ("Appy", version, "http://appyframework.org/pod.html")

        for p in self.installed_plugins:
            for u in p.get_used_libs(html):
                yield u

    def apply_languages(self):
        """This function is called when a Site object gets instantiated,
        i.e. while Django is still loading the settings. It analyzes
        the :attr:`languages` attribute and converts it to a tuple of
        :data:`LanguageInfo` objects.

        """

        if isinstance(self.languages, tuple) \
           and isinstance(self.languages[0], LanguageInfo):
            # e.g. override_defaults() has been called explicitly, without
            # specifying a languages keyword.
            return

        self.language_dict = dict()  # maps simple_code -> LanguageInfo

        self.LANGUAGE_CHOICES = []
        self.LANGUAGE_DICT = dict()  # used in lino.modlib.users
        must_set_language_code = False

        #~ self.AVAILABLE_LANGUAGES = (to_locale(self.DEFAULT_LANGUAGE),)
        if self.languages is None:
            self.languages = [DJANGO_DEFAULT_LANGUAGE]
            #~ self.update_settings(USE_L10N = False)

            #~ info = LanguageInfo(DJANGO_DEFAULT_LANGUAGE,to_locale(DJANGO_DEFAULT_LANGUAGE),0,'')
            #~ self.DEFAULT_LANGUAGE = info
            #~ self.languages = (info,)
            #~ self.language_dict[info.name] = info
        else:
            if isinstance(self.languages, six.string_types):
                self.languages = self.languages.split()
            #~ lc = [x for x in self.django_settings.get('LANGUAGES' if x[0] in languages]
            #~ lc = language_choices(*self.languages)
            #~ self.update_settings(LANGUAGES = lc)
            #~ self.update_settings(LANGUAGE_CODE = lc[0][0])
            #~ self.update_settings(LANGUAGE_CODE = self.languages[0])
            self.update_settings(USE_L10N=True)
            must_set_language_code = True

        languages = []
        for i, django_code in enumerate(self.languages):
            assert_django_code(django_code)
            name = (to_locale(django_code))
            if name in self.language_dict:
                raise Exception("Duplicate name %s for language code %r"
                                % (name, django_code))
            if i == 0:
                suffix = ''
            else:
                suffix = '_' + name
            info = LanguageInfo(str(django_code), str(name), i, str(suffix))
            self.language_dict[name] = info
            languages.append(info)

        new_languages = languages
        for info in tuple(new_languages):
            if '-' in info.django_code:
                base, loc = info.django_code.split('-')
                if not base in self.language_dict:
                    self.language_dict[base] = info

                    # replace the complicated info by a simplified one
                    #~ newinfo = LanguageInfo(info.django_code,base,info.index,info.suffix)
                    #~ new_languages[info.index] = newinfo
                    #~ del self.language_dict[info.name]
                    #~ self.language_dict[newinfo.name] = newinfo

        #~ for base,lst in simple_codes.items():
            #~ if len(lst) == 1 and and not base in self.language_dict:
                #~ self.language_dict[base] = lst[0]

        self.languages = tuple(new_languages)
        self.DEFAULT_LANGUAGE = self.languages[0]

        self.BABEL_LANGS = tuple(self.languages[1:])

        if must_set_language_code:
            self.update_settings(LANGUAGE_CODE=self.languages[0].django_code)
            # Note: LANGUAGE_CODE is what *Django* believes to be the
            # default language.  This should be some variant of
            # English ('en' or 'en-us') if you use
            # `django.contrib.humanize`
            # https://code.djangoproject.com/ticket/20059

        self.setup_languages()

    def setup_languages(self):
        """
        Reduce Django's :setting:`LANGUAGES` to my `languages`.
        Note that lng.name are not yet translated, we take these
        from `django.conf.global_settings`.
        """

        from django.conf.global_settings import LANGUAGES

        def langtext(code):
            for k, v in LANGUAGES:
                if k == code:
                    return v
            # returns None if not found

        def _add_language(code, lazy_text):
            self.LANGUAGE_DICT[code] = lazy_text
            self.LANGUAGE_CHOICES.append((code, lazy_text))

        if self.languages is None:

            _add_language(DJANGO_DEFAULT_LANGUAGE, _("English"))

        else:

            for lang in self.languages:
                code = lang.django_code
                text = langtext(code)
                if text is None:
                    # Django doesn't know these
                    if code == 'de-be':
                        text = gettext_noop("German (Belgium)")
                    elif code == 'de-ch':
                        text = gettext_noop("German (Swiss)")
                    elif code == 'de-at':
                        text = gettext_noop("German (Austria)")
                    elif code == 'en-us':
                        text = gettext_noop("American English")
                    else:
                        raise Exception(
                            "Unknown language code %r (must be one of %s)" % (
                                lang.django_code,
                                [x[0] for x in LANGUAGES]))

                text = _(text)
                _add_language(lang.django_code, text)

            """
            Cannot activate the site's default language
            because some test cases in django.contrib.humanize
            rely on en-us as default language
            """
            #~ set_language(self.get_default_language())

            """
            reduce LANGUAGES to my babel languages:
            """
            self.update_settings(
                LANGUAGES=[x for x in LANGUAGES
                           if x[0] in self.LANGUAGE_DICT])

    def get_language_info(self, code):
        """Use this in Python fixtures or tests to test whether a Site
        instance supports a given language.  `code` must be a
        Django-style language code.
        
        On a site with only one locale of a language (and optionally
        some other languages), you can use only the language code to
        get a tuple of :data:`LanguageInfo` objects.
        
        >>> from lino.core.site import TestSite as Site
        >>> Site(languages="en-us fr de-be de").get_language_info('en')
        LanguageInfo(django_code='en-us', name='en_US', index=0, suffix='')
        
        On a site with two locales of a same language (e.g. 'en-us'
        and 'en-gb'), the simple code 'en' yields that first variant:
        
        >>> site = Site(languages="en-us en-gb")
        >>> print(site.get_language_info('en'))
        LanguageInfo(django_code='en-us', name='en_US', index=0, suffix='')

        """
        return self.language_dict.get(code, None)

    def resolve_languages(self, languages):
        """
        This is used by `UserProfile`.
        
        Examples:
        
        >>> from lino.core.site import TestSite as Site
        >>> lst = Site(languages="en fr de nl et pt").resolve_languages('en fr')
        >>> [i.name for i in lst]
        ['en', 'fr']
        
        You may not specify languages which don't exist on this site:
        
        >>> Site(languages="en fr de").resolve_languages('en nl')
        Traceback (most recent call last):
        ...
        Exception: Unknown language code 'nl' (must be one of ['en', 'fr', 'de'])
        
        
        """
        rv = []
        if isinstance(languages, six.string_types):
            languages = languages.split()
        for k in languages:
            if isinstance(k, six.string_types):
                li = self.get_language_info(k)
                if li is None:
                    raise Exception("Unknown language code %r (must be one of %s)" % (
                        str(k), [li.name for li in self.languages]))
                rv.append(li)
            else:
                assert k in self.languages
                rv.append(k)
        return tuple(rv)

    def language_choices(self, language, choices):
        l = choices.get(language, None)
        if l is None:
            l = choices.get(self.DEFAULT_LANGUAGE)
        return l

    def get_default_language(self):
        """
        The django code of the default language to use in every
        :class:`dd.LanguageField`.
        
        """
        return self.DEFAULT_LANGUAGE.django_code

    def str2kw(self, name, txt,  **kw):
        """
        Return a dictionary which maps the internal field names for
        babelfield `name` to their respective translation of the given
        lazy translatable string `text`.

        >>> from django.utils.translation import ugettext_lazy as _
        >>> from lino.core.site import TestSite as Site
        >>> site = Site(languages='de fr es')
        >>> site.str2kw('name', _("January")) == {'name_fr': 'janvier', 'name': 'Januar', 'name_es': 'Enero'}
        True
        >>> site = Site(languages='fr de es')
        >>> site.str2kw('name', _("January")) == {'name_de': 'Januar', 'name': 'janvier', 'name_es': 'Enero'}
        True
        

        """
        from django.utils import translation
        for simple, info in list(self.language_dict.items()):
            with translation.override(simple):
                # kw[name + info.suffix] = str(txt)
                kw[name + info.suffix] = six.text_type(txt)
        return kw

    def babelkw(self, name, **kw):
        """
        Return a dict with appropriate resolved field names for a
        BabelField `name` and a set of hard-coded values.

        You have some hard-coded multilingual content in a fixture:
        >>> from lino.core.site import TestSite as Site
        >>> kw = dict(de="Hallo", en="Hello", fr="Salut")

        The field names where this info gets stored depends on the
        Site's `languages` distribution.
        
        >>> Site(languages="de-be en").babelkw('name',**kw) == {'name_en': 'Hello', 'name': 'Hallo'}
        True
        
        >>> Site(languages="en de-be").babelkw('name',**kw) == {'name_de_BE': 'Hallo', 'name': 'Hello'}
        True
        
        >>> Site(languages="en-gb de").babelkw('name',**kw) == {'name_de': 'Hallo', 'name': 'Hello'}
        True
        
        >>> Site(languages="en").babelkw('name',**kw) == {'name': 'Hello'}
        True
        
        >>> Site(languages="de-be en").babelkw('name',de="Hallo",en="Hello") == {'name_en': 'Hello', 'name': 'Hallo'}
        True

        In the following example `babelkw` attributes the 
        keyword `de` to the *first* language variant:
        
        >>> Site(languages="de-ch de-be").babelkw('name',**kw) == {'name': 'Hallo'}
        True
        
        
        """
        d = dict()
        for simple, info in self.language_dict.items():
            v = kw.get(simple, None)
            if v is not None:
                d[name + info.suffix] = six.text_type(v)
        return d

    def args2kw(self, name, *args):
        """
        Takes the basename of a BabelField and the values for each language.
        Returns a `dict` mapping the actual fieldnames to their values.
        """
        assert len(args) == len(self.languages)
        kw = {name: args[0]}
        for i, lang in enumerate(self.BABEL_LANGS):
            kw[name + '_' + lang] = args[i + 1]
        return kw

    def field2kw(self, obj, name, **known_values):
        """Return a `dict` with all values of the BabelField `name` in the
given object `obj`. The dict will have one key for each
:attr:`languages`.

        Examples:

        >>> from lino.core.site import TestSite as Site
        >>> from atelier.utils import AttrDict
        >>> def testit(site_languages):
        ...     site = Site(languages=site_languages)
        ...     obj = AttrDict(site.babelkw(
        ...         'name', de="Hallo", en="Hello", fr="Salut"))
        ...     return site,obj


        >>> site, obj = testit('de en')
        >>> site.field2kw(obj, 'name') == {'de': 'Hallo', 'en': 'Hello'}
        True

        >>> site, obj = testit('fr et')
        >>> site.field2kw(obj, 'name') == {'fr': 'Salut'}
        True

        """
        # d = { self.DEFAULT_LANGUAGE.name : getattr(obj,name) }
        for lng in self.languages:
            v = getattr(obj, name + lng.suffix, None)
            if v:
                known_values[lng.name] = v
        return known_values

    def field2args(self, obj, name):
        """
        Return a list of the babel values of this field in the order of
        this Site's :attr:`Site.languages` attribute.
        
        """
        return [getattr(obj, name + li.suffix) for li in self.languages]
        #~ l = [ getattr(obj,name) ]
        #~ for lang in self.BABEL_LANGS:
            #~ l.append(getattr(obj,name+'_'+lang))
        #~ return l

    def babelitem(self, *args, **values):
        """
        Given a dictionary with babel values, return the
        value corresponding to the current language.

        This is available in templates as a function `tr`.

        >>> kw = dict(de="Hallo", en="Hello", fr="Salut")

        >>> from lino.core.site import TestSite as Site
        >>> from django.utils import translation

        A Site with default language "de":

        >>> site = Site(languages="de en")
        >>> tr = site.babelitem
        >>> with translation.override('de'):
        ...    print(tr(**kw))
        Hallo

        >>> with translation.override('en'):
        ...    print(tr(**kw))
        Hello

        If the current language is not found in the specified `values`,
        then it returns the site's default language:

        >>> with translation.override('jp'):
        ...    print(tr(en="Hello", de="Hallo", fr="Salut"))
        Hallo

        Testing detail: default language should be "de" in our example, but
        we are playing here with more than one Site instance while Django
        knows only one "default language" which is the one specified in
        `lino.projects.docs.settings`.

        Another way is to specify an explicit default value using a
        positional argument. In that case the language's default language
        doesn'n matter:

        >>> with translation.override('jp'):
        ...    print(tr("Tere", de="Hallo", fr="Salut"))
        Tere

        >>> with translation.override('de'):
        ...     print(tr("Tere", de="Hallo", fr="Salut"))
        Hallo

        You may not specify more than one default value:

        >>> tr("Hello", "Hallo")
        Traceback (most recent call last):
        ...
        ValueError: ('Hello', 'Hallo') is more than 1 default value.


        """
        if len(args) == 0:
            info = self.language_dict.get(
                get_language(), self.DEFAULT_LANGUAGE)
            default_value = None
            if info == self.DEFAULT_LANGUAGE:
                return values.get(info.name)
            x = values.get(info.name, None)
            if x is None:
                return values.get(self.DEFAULT_LANGUAGE.name)
            return x
        elif len(args) == 1:
            info = self.language_dict.get(get_language(), None)
            if info is None:
                return args[0]
            default_value = args[0]
            return values.get(info.name, default_value)
        args = tuple_py2(args)
        # print(type(args))
        raise ValueError("%(values)s is more than 1 default value." %
                         dict(values=args))

    # babel_get(v) = babelitem(**v)

    def babeldict_getitem(self, d, k):
        v = d.get(k, None)
        if v is not None:
            assert type(v) is dict
            return self.babelitem(**v)

    def babelattr(self, obj, attrname, default=NOT_PROVIDED, language=None):
        """
        Return the value of the specified babel field `attrname` of `obj`
        in the current language.

        This is to be used in multilingual document templates.  For
        example in a document template of a Contract you may use the
        following expression::

          babelattr(self.type, 'name')

        This will return the correct value for the current language.

        Examples:

        >>> from __future__ import unicode_literals
        >>> from django.utils import translation
        >>> from lino.core.site import TestSite as Site
        >>> from atelier.utils import AttrDict
        >>> def testit(site_languages):
        ...     site = Site(languages=site_languages)
        ...     obj = AttrDict(site.babelkw(
        ...         'name', de="Hallo", en="Hello", fr="Salut"))
        ...     return site, obj


        >>> site,obj = testit('de en')
        >>> with translation.override('de'):
        ...     print(site.babelattr(obj,'name'))
        Hallo

        >>> with translation.override('en'):
        ...     print(site.babelattr(obj,'name'))
        Hello

        If the object has no translation for a given language, return
        the site's default language.  Two possible cases:

        The language exists on the site, but the object has no
        translation for it:

        >>> site,obj = testit('en es')
        >>> with translation.override('es'):
        ...     print(site.babelattr(obj, 'name'))
        Hello

        Or a language has been activated which doesn't exist on the site:

        >>> with translation.override('fr'):
        ...     print(site.babelattr(obj, 'name'))
        Hello


        """
        if language is None:
            language = get_language()
        info = self.language_dict.get(language, self.DEFAULT_LANGUAGE)
        if info.index != 0:
            v = getattr(obj, attrname + info.suffix, None)
            if v:
                return v
        if default is NOT_PROVIDED:
            return getattr(obj, attrname)
        else:
            return getattr(obj, attrname, default)
        #~ if lang is not None and lang != self.DEFAULT_LANGUAGE:
            #~ v = getattr(obj,attrname+"_"+lang,None)
            #~ if v:
                #~ return v
        #~ return getattr(obj,attrname,*args)

    def diagnostic_report_rst(self, *args):
        """Returns a string with a diagnostic report about this
site. :manage:`diag` is a command-line shortcut to this.

        """
        s = ''
        s += rstgen.header(1, "Plugins")
        for n, kp in enumerate(self.plugins.items()):
            s += "%d. " % (n + 1)
            s += "%s : %s\n" % kp
        # s += "config_dirs: %s\n" % repr(self.confdirs.config_dirs)
        s += "\n"
        s += rstgen.header(1, "Config directories")
        for n, cd in enumerate(self.confdirs.config_dirs):
            s += "%d. " % (n + 1)
            ln = relpath(cd.name)
            if cd.writeable:
                ln += " [writeable]"
            s += ln + '\n'
        # for arg in args:
        #     p = self.plugins[arg]
        return s

    # def get_db_overview_rst(self):
    #     from lino.utils.diag import analyzer
    #     analyzer.show_db_overview()

    def override_defaults(self, **kwargs):
        self.override_settings(**kwargs)
        self.install_settings()

    def is_imported_partner(self, obj):
        """
        Return whether the specified
        :class:`Partner <ml.contacts.Partner>` instance
        `obj` is to be considered as imported from some legacy database.
        """
        #~ return obj.id is not None and (obj.id < 200000 or obj.id > 299999)
        return False
        #~ return obj.id is not None and (obj.id > 10 and obj.id < 21)

    def site_header(self):
        """Used in footnote or header of certain printed documents.

        The convention is to call it as follows from an appy.pod template
        (use the `html` function, not `xhtml`)
        ::

          do text
          from html(settings.SITE.site_header())

        Note that this is expected to return a unicode string possibly
        containing valid HTML (not XHTML) tags for formatting.

        """
        if self.is_installed('contacts'):
            if self.site_config.site_company:
                return self.site_config.site_company.get_address('<br/>')
                #~ s = unicode(self.site_config.site_company) + " / "  + s
        #~ return ''

    def setup_main_menu(self):
        """
        To be implemented by applications.
        """
        pass

    @property
    def site_config(self):
        """
        This property holds a cached version of the one and only
        :class:`ml.system.SiteConfig` row that holds site-wide
        database-stored and web-editable Site configuration parameters.

        If no instance exists (which happens in a virgin database), we
        create it using default values from :attr:`site_config_defaults`.

        This is always `None` when :mod:`lino.modlib.system` is not installed.

        """
        if 'system' not in self.models:
            return None

        if self._site_config is None:
            #~ raise Exception(20130301)
            #~ print '20130320 create _site_config'
            #~ from lino.core.utils import resolve_model
            #~ from lino.core.utils import obj2str
            #~ from lino.utils import dblogger as logger
            #~ SiteConfig = resolve_model('system.SiteConfig')
            SiteConfig = self.models.system.SiteConfig
            #~ from .models import SiteConfig
            #~ from django.db.utils import DatabaseError
            try:
                #~ self._site_config = SiteConfig.real_objects.get(pk=1)
                self._site_config = SiteConfig.real_objects.get(
                    pk=self.config_id)
                #~ print "20130301 Loaded SiteConfig record", obj2str(self._site_config,True)
            #~ except (SiteConfig.DoesNotExist,DatabaseError):
            except SiteConfig.DoesNotExist:
            #~ except Exception,e:
                kw = dict(pk=self.config_id)
                #~ kw.update(settings.SITE.site_config_defaults)
                kw.update(self.site_config_defaults)
                self._site_config = SiteConfig(**kw)
                #~ print "20130301 Created SiteConfig record", obj2str(self._site_config,True)
                # 20120725
                # polls_tutorial menu selection `Config --> Site Parameters`
                # said "SiteConfig 1 does not exist"
                # cannot save the instance here because the db table possibly doesn't yet exit.
                #~ self._site_config.save()
        return self._site_config
    #~ site_config = property(get_site_config)

    #~ def shutdown(self):
        #~ self.clear_site_config()
        #~ return super(Site,self).shutdown()

    def clear_site_config(self):
        """
        Clear the cached SiteConfig instance.

        This is needed e.g. when the test runner has created a new
        test database.
        """
        self._site_config = None
        #~ print "20130320 clear_site_config"

    def get_quicklinks(self, ar):
        from lino.core import menus
        m = menus.Toolbar(ar.get_user().profile, 'quicklinks')
        self.setup_quicklinks(ar, m)
        return m

    def get_site_menu(self, ui, profile):
        """
        Return this site's main menu for the given UserProfile.
        Must be a :class:`lino.core.menus.Toolbar` instance.
        Applications usually should not need to override this.
        """
        from lino.core import menus
        main = menus.Toolbar(profile, 'main')
        self.setup_menu(profile, main)
        main.compress()
        return main

    def setup_quicklinks(self, ar, m):
        """
        Override this
        in application-specific (or even local) :xfile:`settings.py` files
        to define a series of *quick links* to appear below the main menu bar.
        Example see :meth:`lino.projects.pcsw.settings.Site.setup_quicklinks`.
        """
        self.on_each_app('setup_quicklinks', ar, m)

    def setup_menu(self, profile, main):
        """Set up the application's menu structure.

        The default implementation uses a system of predefined
        top-level items that are filled by the different installed
        plugins.

        - `setup_master_menu`
        - `setup_main_menu`
        - `setup_reports_menu`
        - `setup_config_menu`
        - `setup_explorer_menu`
        - `setup_site_menu`


        """
        if AFTER17:
            from django.apps import apps
            apps = [a.models_module for a in apps.get_app_configs()]
        else:
            from django.db.models import loading
            apps = loading.get_apps()

        for k, label in self.top_level_menus:
            methname = "setup_{0}_menu".format(k)

            for mod in apps:
                if hasattr(mod, methname):
                    msg = "{0} still has a function {1}(). \
Please convert to Plugin method".format(mod, methname)
                    raise Exception(msg)

            if label is None:
                menu = main
            else:
                menu = main.add_menu(k, label)
            for p in self.installed_plugins:
                meth = getattr(p, methname, None)
                if meth is not None:
                    meth(self, profile, menu)

    def get_middleware_classes(self):
        """Yields the strings to be stored in
        the :setting:`MIDDLEWARE_CLASSES` setting.

        In case you don't want to use this method for defining
        :setting:`MIDDLEWARE_CLASSES`, you can simply set
        :setting:`MIDDLEWARE_CLASSES` in your :xfile:`settings.py`
        after the :class:`Site` has been instantiated.

        `Django and standard HTTP authentication
        <http://stackoverflow.com/questions/152248/can-i-use-http-basic-authentication-with-django>`_

        """

        yield 'django.middleware.common.CommonMiddleware'
        #~ yield 'django.contrib.sessions.middleware.SessionMiddleware'
        if self.languages and len(self.languages) > 1:
            yield 'django.middleware.locale.LocaleMiddleware'
        #~ yield 'django.contrib.auth.middleware.AuthenticationMiddleware'
        #~ if self.user_model:
        #~ if self.user_model is None:
            #~ yield 'lino.core.auth.NoUserMiddleware'

        if self.auth_middleware:
            yield self.auth_middleware
        else:
            if self.user_model is None:
                yield 'lino.core.auth.NoUserMiddleware'
            elif self.default_user:
                if self.default_user == "anonymous":
                    yield 'lino.core.auth.NoUserMiddleware'
                else:
                    yield 'lino.core.auth.DefaultUserMiddleware'
            elif self.remote_user_header:
                yield 'lino.core.auth.RemoteUserMiddleware'
            else:
                # not using remote http auth, so we need sessions
                yield 'django.contrib.sessions.middleware.SessionMiddleware'
                if self.ldap_auth_server:
                    yield 'lino.core.auth.LDAPAuthMiddleware'
                else:
                    yield 'lino.core.auth.SessionUserMiddleware'

                #~ raise Exception("""\
    #~ `user_model` is not None, but no `remote_user_header` in your settings.SITE.""")
        #~ yield 'lino.utils.editing.EditingMiddleware'
        if True:
            yield 'lino.utils.ajax.AjaxExceptionResponse'

        if False:  # not BYPASS_PERMS:
            yield 'django.contrib.auth.middleware.RemoteUserMiddleware'
            # TODO: find solution for this:
            #~ AUTHENTICATION_BACKENDS = (
              #~ 'django.contrib.auth.backends.RemoteUserBackend',
            #~ )

        if False:
            #~ yield 'lino.utils.sqllog.ShortSQLLogToConsoleMiddleware'
            yield 'lino.utils.sqllog.SQLLogToConsoleMiddleware'
            #~ yield 'lino.utils.sqllog.SQLLogMiddleware'

    # def get_main_action(self, profile):
    #     """No longer used.
    #     Return the action to show as top-level "index.html".
    #     The default implementation returns `None`, which means
    #     that Lino will call :meth:`get_main_html`.
    #     """
    #     return None

    def get_main_html(self, request, **context):
        """Return a chunk of html to be displayed in the main area of the
        admin index.  This is being called only if
        :meth:`get_main_action` returns `None`.  The default
        implementation renders the :xfile:`admin_main.html` template.

        """
        return self.plugins.jinja.render_from_request(
            request, 'admin_main.html', **context)

    def get_welcome_messages(self, ar):
        """
        Yields a list of "welcome messages" (see
        :meth:`lino.core.actors.Actor.get_welcome_messages`) of all
        actors.  This is being called from :xfile:`admin_main.html`.
        """

        for h in self._welcome_handlers:
            for msg in h(ar):
                yield msg
        # for a in self._welcome_actors:
        #     for msg in a.get_welcome_messages(ar):
        #         yield msg

    def add_welcome_handler(self, func):
        """Add the given callable as a "welcome handler".  Lino will call
        every welcome handler for every incoming request, passing them
        a :class:`BaseRequest <lino.core.requests.BaseRequest>`
        instance representing this request as positional argument.
        The callable is expected to yield a series of messages
        (usually either 0 or 1). Each message must be either a string
        or a :class:`E.span <lino.utils.xmlgen.html.E>` element.

        """
        self._welcome_handlers.append(func)

    def get_installed_apps(self):
        """Yield the list of apps to be installed on this site.  Each item
        must be either a string (unicode being converted to str) or a
        *generator* which will be iterated recursively (again
        expecting either strings or generators of strings).

        Lino will call this method exactly once when the :class:`Site`
        instantiates.  The resulting list of names will then possibly
        altered by the :meth:`get_apps_modifiers` method before being
        assigned to the :setting:`INSTALLED_APPS` setting.

        """

        if self.django_admin_prefix:
            yield 'django.contrib.admin'  # not tested

        yield 'django.contrib.staticfiles'
        yield 'lino.modlib.about'

        yield self.default_ui
        # if self.default_ui == "extjs":
        #     yield 'lino.modlib.extjs'
        #     yield 'lino.modlib.bootstrap3'
        # elif self.default_ui == "bootstrap3":
        #     yield 'lino.modlib.bootstrap3'

        for a in self.local_apps:
            yield a

        # yield "lino.modlib.lino_startup"

    site_prefix = '/'
    """The string to prefix to every URL of the Lino web interface.

    This must *start and end with a *slash*.  Default value is
    ``'/'``.

    This must be set if your project is not being served at the "root"
    URL of your server.

    If this is different from the default value, Lino also sets
    :setting:`SESSION_COOKIE_PATH`.

    When this Site is running under something else than a development
    server, this setting must correspond to your web server's
    configuration.  For example if you have::
    
        WSGIScriptAlias /foo /home/luc/mypy/lino_sites/foo/wsgi.py
      
    Then your :xfile:`settings.py` should specify::
    
        site_prefix = '/foo/'
    
    See also :ref:`mass_hosting`.

    """

    def buildurl(self, *args, **kw):
        url = self.site_prefix + ("/".join(args))
        if len(kw):
            url += "?" + urlencode(kw, True)
        return url

    def build_media_url(self, *args, **kw):
        from django.conf import settings
        url = settings.MEDIA_URL + ("/".join(args))
        if len(kw):
            url += "?" + urlencode(kw, True)
        return url

    def build_static_url(self, *args, **kw):
        from django.conf import settings
        url = settings.STATIC_URL + ("/".join(args))
        if len(kw):
            url += "?" + urlencode(kw, True)
        return url

    def get_system_note_recipients(self, request, obj, silent):
        """Return or yield a list of recipients
        (i.e. strings like "John Doe  <john@example.com>" )
        to be notified by email about a system note issued
        by action request `ar` about the object instance `obj`.

        Default behaviour is to simply forward it to the `obj`'s
        :meth:`get_system_note_recipients
        <lino.core.model.Model.get_system_note_recipients>`, but here
        is a hook to define local exceptions to the application
        specific default rules.

        """
        return obj.get_system_note_recipients(request, silent)

    def emit_system_note(self, request, owner, subject, body, silent):
        """Send a *system note* about the given model instance `owner` with
        the given `subject` and `body` .

        A **system note** is a text message attached to a given
        database object (`owner`) which is stored and propagated
        through a series of customizable and configurable channels.

        The text part consists basically of a subject and a body, both
        usually generated by the application and possibly edited by
        the user (e.g. in the dialog window of a
        :class:`NotifyingAction <lino.core.actions.NotifyingAction>`).

        This method will build the list of email recipients by calling
        the locally configurable :meth:`get_system_note_recipients`
        method and send an email to each of these recipients.

        """
        # self.logger.info("20121016 add_system_note() '%s'",subject)

        if self.is_installed('notes'):
            notes = self.models.notes
            notes.add_system_note(request, owner, subject, body)
        sender = request.user.email or self.django_settings['SERVER_EMAIL']
        if not sender or '@example.com' in sender:
            return
        recipients = self.get_system_note_recipients(request, owner, silent)
        self.send_email(subject, sender, body, recipients)

    def send_email(self, subject, sender, body, recipients):
        """Send an email message with the specified arguments (the same
signature as `django.core.mail.EmailMessage`.

        `recipients` is an iterator over a list of strings with email
        addresses. Any address containing '@example.com' will be
        removed. Does nothing if the resulting list of recipients is
        empty.

        If `body` starts with "<", then it is considered to be HTML.

        """
        if '@example.com' in sender:
            self.logger.info(
                "Ignoring email '%s' because sender is %s", subject, sender)
            return
        recipients = [a for a in recipients if '@example.com' not in a]
        if not len(recipients):
            self.logger.info(
                "Ignoring email '%s' because there is no recipient", subject)
            return

        self.logger.info(
            "Send email '%s' from %s to %s", subject, sender, recipients)

        from django.core.mail import send_mail
        kw = {}
        if body.startswith('<'):
            kw['html_message'] = body
            body = html2text(body)
        send_mail(subject, body, sender, recipients, **kw)

        # msg = EmailMessage(subject=subject,
        #                    from_email=sender, body=body, to=recipients)

        # from django.core.mail import EmailMessage
        
        # msg = EmailMessage(subject=subject,
        #                    from_email=sender, body=body, to=recipients)
        # self.logger.info(
        #     "Send email '%s' from %s to %s", subject, sender, recipients)
        # msg.send()

    def welcome_html(self, ui=None):
        """
        Return a HTML version of the "This is APPLICATION
        version VERSION using ..." text. to be displayed in the
        About dialog, in the plain html footer, and maybe at other
        places.

        """
        from django.utils.translation import ugettext as _

        p = []
        sep = ''
        if self.verbose_name:
            p.append(_("This is "))
            if self.url:
                p.append(
                    E.a(self.verbose_name, href=self.url, target='_blank'))
            else:
                p.append(E.b(self.verbose_name))
            if self.version:
                p.append(' ')
                p.append(self.version)
            sep = _(' using ')

        for name, version, url in self.get_used_libs(html=E):
            p.append(sep)
            p.append(E.a(name, href=url, target='_blank'))
            p.append(' ')
            p.append(version)
            sep = ', '
        return E.span(*p)

    def login(self, username=None, **kw):
        """Open a session as the user with the given `username`.
    
        For usage from a shell or a tested document.  Does not require
        any password because when somebody has command-line access we
        trust that she has already authenticated.
    
        It returns a
        :class:`BaseRequest <lino.core.requests.BaseRequest>` object.

        """
        from lino.core import requests
        self.startup()
        User = self.user_model
        if User and username:
            try:
                kw.update(user=User.objects.get(username=username))
            except User.DoesNotExist:
                raise Exception("'{0}' : no such user".format(username))

        # if not 'renderer' in kw:
        #     kw.update(renderer=self.ui.text_renderer)

        # import lino.core.urls  # hack: trigger ui instantiation
        return requests.BaseRequest(**kw)

    def get_letter_date_text(self, today=None):
        """Returns a string like "Eupen, den 26. August 2013".

        """
        sc = self.site_config.site_company
        if today is None:
            today = self.today()
        from lino.utils.format_date import fdl
        if sc and sc.city:
            return _("%(place)s, %(date)s") % dict(
                place=str(sc.city.name), date=fdl(today))
        return fdl(today)

    def get_admin_main_items(self, ar):
        """Expected to yield a sequence of "items" to be rendered on the home
        page (:xfile:`admin_main.html`).

        Every item is expected to be a :class:`dd.Table` or a
        :class:`dd.VirtualTable`. These tables are rendered in that order,
        with a limit of :attr:`dd.AbstractTable.preview_limit` rows.

        """
        return []

    def decfmt(self, v, places=2, **kw):
        """ Format a Decimal value using :func:`lino.utils.moneyfmt`, but
        applying the site settings
        :attr:`lino.Lino.decimal_group_separator` and
        :attr:`lino.Lino.decimal_separator`.

        >>> from lino.core.site import TestSite as Site
        >>> from decimal import Decimal
        >>> self = Site()
        >>> print(self.decimal_group_separator)
        \xa0
        >>> print(self.decimal_separator)
        ,

        >>> x = Decimal(1234)
        >>> print(self.decfmt(x))
        1\xa0234,00

        >>> print(self.decfmt(x, sep="."))
        1.234,00

        >>> self.decimal_group_separator = '.'
        >>> print(self.decfmt(x))
        1.234,00
        
        >>> self.decimal_group_separator = "oops"
        >>> print(self.decfmt(x))
        1oops234,00
        

        """
        kw.setdefault('sep', self.decimal_group_separator)
        kw.setdefault('dp', self.decimal_separator)
        from lino.utils import moneyfmt
        return moneyfmt(v, places=places, **kw)

    LOOKUP_OP = '__iexact'

    def lookup_filter(self, fieldname, value, **kw):
        """
        Return a `models.Q` to be used if you want to search for a given 
        string in any of the languages for the given babel field.
        """
        from django.db.models import Q
        kw[fieldname + self.LOOKUP_OP] = value
        #~ kw[fieldname] = value
        flt = Q(**kw)
        del kw[fieldname + self.LOOKUP_OP]
        for lng in self.BABEL_LANGS:
            kw[fieldname + lng.suffix + self.LOOKUP_OP] = value
            flt = flt | Q(**kw)
            del kw[fieldname + lng.suffix + self.LOOKUP_OP]
        return flt

    def relpath(self, p):
        """Used by :class:`lino.mixins.printable.EditTemplate` in order to
        write a testable message...

        """
        if p.startswith(self.project_dir):
            p = "$(PRJ)" + p[len(self.project_dir):]
        return p


class TestSite(Site):

    """Used to simplify doctest strings because it inserts default values
    for the two first arguments that are mandatory but not used in our
    examples::
    
    >> from lino.core.site import Site
    >> Site(globals(), ...)
    
    >> from lino.core.site import TestSite as Site
    >> Site(...)

    """

    def __init__(self, *args, **kwargs):
        # kwargs.update(no_local=True)
        g = dict(__file__=__file__)
        g.update(SECRET_KEY="20227")  # see :djangoticket:`20227`
        super(TestSite, self).__init__(g, *args, **kwargs)

        # 20140913 Hack needed for doctests in :mod:`ad`.
        from django.utils import translation
        translation._default = None


def _test():
    # we want to raise an Exception if there is a failure, but
    # doctest's raise_on_error=True option is not useful because it
    # does not report the traceback if some test fails.
    import doctest
    res = doctest.testmod()
    if res.failed > 0:
        raise Exception("{0} (see earlier output)".format(res))
        

if __name__ == "__main__":
    _test()
