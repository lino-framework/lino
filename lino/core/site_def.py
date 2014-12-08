# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre.
# License: BSD, see LICENSE for more details.

"""
This defines the  :class:`Plugin` and  :class:`Site` classes.

"""

# from __future__ import unicode_literals
# from __future__ import print_function

# import logging
# logger = logging.getLogger(__name__)

import os
from os.path import normpath, dirname, join, isdir, abspath, relpath
import inspect
import datetime
import warnings
import codecs
import collections
from urllib import urlencode

from atelier.utils import AttrDict, ispure, date_offset

from django.utils.translation import ugettext_lazy as _

from .plugin import Plugin

from lino import assert_django_code, DJANGO_DEFAULT_LANGUAGE
from lino.utils.xmlgen.html import E


LanguageInfo = collections.namedtuple(
    'LanguageInfo', ('django_code', 'name', 'index', 'suffix'))


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


gettext_noop = lambda s: s

PLUGIN_CONFIGS = {}


def configure_plugin(app_label, **kwargs):
    cfg = PLUGIN_CONFIGS.setdefault(app_label, {})
    cfg.update(kwargs)


class NOT_PROVIDED:
    pass


class Site(object):
    """This is the base for every Lino Site.

    Instantiating this class in a :xfile:`settings.py` file will
    automatically set default values for Django's
    :setting:`SERIALIZATION_MODULES` :setting:`FIXTURE_DIRS` settings.

    See :class:`dd.Site`.

    See also:

    - :doc:`/usage`
    - :doc:`/settings`
    - :ref:`application`
    """

    the_demo_date = None
    verbose_name = None  # "Unnamed Lino Application"
    version = None
    url = None
    make_missing_dirs = True
    userdocs_prefix = ''
    project_name = None
    project_dir = None
    languages = ''

    site_config = None  # Overridden by `lino.lino_site.Site.site_config`.
    not_found_msg = '(not installed)'
    django_settings = None
    startup_time = None
    plugins = None
    modules = AttrDict()

    is_local_project_dir = False
    """
    This is automatically set when a :class:`Site` is instantiated. 
    Don't override it.
    Contains `True` if this is a "local" project.
    For local projects, Lino checks for local fixtures and config directories
    and adds them to the default settings.
    """

    loading_from_dump = False

    # see docs/settings.rst
    migration_class = None
    languages = None
    hidden_languages = None

    BABEL_LANGS = tuple()

    partners_app_label = 'contacts'
    """
    Temporary setting, see :ref:`polymorphism`.
    """

    # three constants used by lino.modlib.workflows:
    max_state_value_length = 20
    max_action_name_length = 50
    max_actor_name_length = 100

    trusted_templates = False

    allow_duplicate_cities = False

    uid = 'myuid'
    """A universal identifier for this Site.  This is needed when
    synchronizing with CalDAV server.  Locally created calendar
    components in remote calendars will get a UID based on this
    parameter, using ``"%s@%s" (self.pk, settings.SITE.ui)``.
    
    The default value is ``'myuid'``, and you should certainly
    override this on a production server that uses remote calendars.

    """

    project_model = None

    #~ user_model = "users.User"
    user_model = None

    auth_middleware = None

    legacy_data_path = None

    propvalue_max_length = 200
    """
    Used by :mod:`lino.modlib.properties`.
    """

    never_build_site_cache = False
    show_internal_field_names = False
    build_js_cache_on_startup = False
    use_java = True
    use_experimental_features = False
    site_config_defaults = {}

    default_build_method = "appypdf"

    is_demo_site = True
    demo_email = 'demo@example.com'
    demo_fixtures = ['std', 'demo', 'demo2']

    use_spinner = False  # doesn't work. leave this to False

    #~ django_admin_prefix = '/django'
    django_admin_prefix = None
    """
    The prefix to use for Django admin URLs.
    Leave this unchanged as long as :doc:`/tickets/70` is not solved.
    """

    start_year = 2011
    time_format_extjs = 'H:i'
    date_format_extjs = 'd.m.Y'
    alt_date_formats_extjs = 'd/m/Y|Y-m-d'
    #~ default_number_format_extjs = '0,000.00/i'
    default_number_format_extjs = '0,00/i'

    uppercase_last_name = False

    tinymce_base_url = "http://www.tinymce.com/js/tinymce/jscripts/tiny_mce/"
    "Similar to :attr:`extjs_base_url` but pointing to http://www.tinymce.com."

    jasmine_root = None
    """
    Path to the Jasmine root directory.
    Only used on a development server
    if the `media` directory has no symbolic link to the Jasmine root directory
    and only if :attr:`use_jasmine` is True.
    """

    tinymce_root = None
    """
    Path to the tinymce root directory.
    Only to be used on a development server
    if the `media` directory has no symbolic link to the TinyMCE root directory,
    and only if :attr:`use_tinymce` is True.
    """

    default_user = None
    anonymous_user_profile = '000'
    #~ remote_user_header = "REMOTE_USER"
    remote_user_header = None
    ldap_auth_server = None

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
    """
    Whether to use TinyMCE instead of Ext.form.HtmlEditor. 
    See also :attr:`tinymce_root`.
    See `/blog/2011/0523`.
    """

    use_jasmine = False
    """
    Whether to use the `Jasmine <https://github.com/pivotal/jasmine>`_ testing library.
    """

    use_quicktips = True
    """
    Whether to make use of `Ext.QuickTips
    <http://docs.sencha.com/ext-js/3-4/#!/api/Ext.QuickTips>`_
    when displaying :ref:`help_texts`.
    
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
    Default is "PROJECT_DIR/media/webdav".
    """

    webdav_url = None
    """
    The URL prefix for webdav files.
    In a normal production configuration you should leave this to `None`, 
    Lino will set a default value "/media/webdav/",
    supposing that your Apache is configured as described in 
    :doc:`/admin/webdav`.
    
    This may be used to simulate a :term:`WebDAV` location 
    on a development server.
    For example on a Windows machine, you may set it to ``w:\``,      
    and before invoking :term:`runserver`, you issue in a command prompt::
    
        subst w: <dev_project_path>\media\webdav
        
    """
    sidebar_width = 0

    config_id = 1

    preview_limit = 15

    default_ui = 'extjs'

    textfield_format = 'plain'
    """
    The default format for text fields.
    Valid choices are currently 'plain' and 'html'.

    Text fields are either Django's `models.TextField`
    or :class:`lino.fields.RichTextField`.

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

    verbose_client_info_message = False

    help_url = "http://www.lino-framework.org"
    help_email = "users@lino-framework.org"
    title = "Unnamed Lino site"

    catch_layout_exceptions = True
    """
    Lino usually catches any exception during 
    :meth:`lino.ui.extjs3.ExtUI.create_layout_element`
    to report errors of style 
    "Unknown element "postings.PostingsByController ('postings')" 
    referred in layout <PageDetail on pages.Pages>."
    
    Setting this to `False` is
    useful when there's some problem *within* the framework.
    
    """

    csv_params = dict()
    """
    Site-wide default parameters for CSV generation.
    This must be a dictionary that will be used 
    as keyword parameters to Python `csv.writer()
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

    auto_configure_logger_names = 'atelier lino'

    appy_params = dict(ooPort=8100)
    """
    Used by :class:`lino.mixins.printable.AppyBuildMethod`.
    """

    #~ decimal_separator = '.'
    decimal_separator = ','
    """
    Set this to either ``'.'`` or ``','`` to define wether to use 
    comma or dot as decimal point separator when entering 
    a `DecimalField`.
    """

    #~ decimal_group_separator = ','
    decimal_group_separator = ' '
    """
    Decimal group separator for :func:`lino.utils.moneyfmt`.
    """

    time_format_strftime = '%H:%M'
    date_format_strftime = '%d.%m.%Y'
    date_format_regex = "/^[0123]?\d\.[01]?\d\.-?\d+$/"
    datetime_format_strftime = '%Y-%m-%dT%H:%M:%S'
    datetime_format_extjs = 'Y-m-d\TH:i:s'

    ignore_dates_before = None
    ignore_dates_after = datetime.date.today() + datetime.timedelta(days=5*365)

    # for internal use:
    _welcome_actors = []
    _site_config = None
    _logger = None

    def __init__(self, settings_globals, user_apps=[], **kwargs):
        """
        Every Lino application calls this once in it's
        :file:`settings.py` file.
        See :doc:`/usage`.
        """
        # self.logger.info("20140226 Site.__init__() a %s", self)
        #~ print "20130404 ok?"
        self.init_before_local(settings_globals, user_apps)
        no_local = kwargs.pop('no_local', False)
        if not no_local:
            self.run_djangosite_local()
        self.override_defaults(**kwargs)
        self.load_plugins()
        #~ self.apply_languages()
        self.setup_plugins()
        # self.logger.info("20140226 djangosite.Site.__init__() b")
        # if len(self.logger.handlers) == 0:
        #     raise Exception(self.logger.name)
        from lino.utils.config import ConfigDirCache
        self.confdirs = ConfigDirCache(self)

        assert not self.help_url.endswith('/')

    def run_djangosite_local(self):
        """
        See :doc:`/djangosite_local`
        """
        try:
            from djangosite_local import setup_site
        except ImportError:
            pass
        else:
            setup_site(self)

    def init_before_local(self, settings_globals, user_apps):
        """
        If your `project_dir` contains no :file:`models.py`,
        but *does* contain a `fixtures` subdir,
        then Lino automatically adds this as "local fixtures directory"
        to Django's `FIXTURE_DIRS`.
        """
        if isinstance(user_apps, basestring):
            user_apps = [user_apps]
        if not isinstance(settings_globals, dict):
            raise Exception("""
            Oops, the first argument when instantiating a %s 
            must be your settings.py file's `globals()`
            and not %r
            """ % (self.__class__.__name__, settings_globals))

        if isinstance(user_apps, basestring):
            user_apps = [user_apps]
        #~ self.django_settings = dict()
        #~ self.django_settings.update(settings_globals)
        self.django_settings = settings_globals
        project_file = settings_globals['__file__']

        #~ memory_db = kwargs.pop('memory_db',False)
        #~ nolocal = kwargs.pop('nolocal',False)

        #~ if django_settings.has_key('LINO'):
            #~ raise Exception("Oops: rename settings.LINO to settings.SITE")
        #~ if django_settings.has_key('Lino'):
            #~ raise Exception("Oops: rename settings.Lino to settings.Site")
        self.user_apps = user_apps
        self.project_dir = normpath(dirname(project_file))
        self.project_name = os.path.split(self.project_dir)[-1]

        #~ self.qooxdoo_prefix = '/media/qooxdoo/lino_apps/' + self.project_name + '/build/'
        #~ self.dummy_messages = set()
        self._starting_up = False
        self._startup_done = False

        #~ self._response = None
        self.startup_time = datetime.datetime.now()

        dbname = join(self.project_dir, 'default.db')
        #~ if memory_db:
            #~ dbname  = ':memory:'
        self.django_settings.update(DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': dbname
            }
        })

        #~ self.django_settings.update(SECRET_KEY="20227")
        # see :djangoticket:`20227`

        #~ django_settings.update(FORMAT_MODULE_PATH = 'djangosite.formats')
        #~ django_settings.update(LONG_DATE_FORMAT = "l, j F Y")
        #~ django_settings.update(LONG_DATE_FORMAT = "l, F j, Y")

        self.update_settings(SERIALIZATION_MODULES={
            "py": "lino.utils.dpy",
        })

        modname = self.__module__
        i = modname.rfind('.')
        if i != -1:
            modname = modname[:i]
        self.is_local_project_dir = not modname in self.user_apps

        def settings_subdirs(name):
            lst = []
            for p in self.get_settings_subdirs(name):
                if not os.path.exists(os.path.join(p, '..', 'models.py')):
                    lst.append(p.replace(os.sep, "/"))
            return lst

        self.update_settings(FIXTURE_DIRS=tuple(settings_subdirs('fixtures')))
        self.update_settings(LOCALE_PATHS=tuple(settings_subdirs('locale')))

        self.VIRTUAL_FIELDS = []

        self.update_settings(
            LOGGING_CONFIG='lino.utils.log.configure',
            LOGGING=dict(
                filename=None,
                level='INFO',
                logger_names=self.auto_configure_logger_names,
                disable_existing_loggers=True,  # Django >= 1.5
            ),
        )

    override_modlib_models = None

    def is_abstract_model(self, module_name, model_name):
        "See :func:`dd.is_abstract_model`."
        name = '.'.join(module_name.split('.')[:-1])
        name += '.' + model_name
        rv = name in self.override_modlib_models
        # self.logger.info("20140825 is_abstract_model %s -> %s", name, rv)
        return rv

    def get_apps_modifiers(self, **kw):
        "See :meth:`dd.Site.get_apps_modifiers`."
        return kw

    def load_plugins(self):
        # Called internally during `__init__` method.

        from django.utils.importlib import import_module

        installed_apps = []
        apps_modifiers = self.get_apps_modifiers()

        if hasattr(self, 'hidden_apps'):
            raise Exception("Replace hidden_apps by get_apps_modifiers()")

        def add(x):
            if isinstance(x, basestring):
                app_label = x.split('.')[-1]
                x = apps_modifiers.get(app_label, x)
                if x:
                    # convert unicode to string
                    installed_apps.append(str(x))
            else:
                # if it's not a string, then it's an iterable of strings
                for xi in x:
                    add(xi)
        for x in self.get_installed_apps():
            add(x)
        # add('djangosite')

        plugins = []
        auto_apps = []
        self.plugins = AttrDict()

        def install_plugin(app_name, needed_by=None):
            app_mod = import_module(app_name)
            app_class = getattr(app_mod, 'Plugin', None)
            if app_class is None:
                app_class = Plugin
            # print "Loading plugin", app_name
            k = app_name.rsplit('.')[-1]
            if k in self.plugins:
                txt = self.plugins[k]
                raise Exception("Tried to install '%s' where '%s' "
                                "is already installed." % (
                                    app_name, txt))
            p = app_class(self, k, app_name, app_mod, needed_by)
            cfg = PLUGIN_CONFIGS.pop(k, None)
            if cfg:
                p.configure(**cfg)
            plugins.append(p)
            self.plugins.define(k, p)
            for dep in p.needs_plugins:
                k = dep.rsplit('.')[-1]
                if not k in self.plugins:
                    install_plugin(dep, needed_by=p)
                    auto_apps.append(dep)

        for app_name in installed_apps:
            install_plugin(app_name)

        installed_apps.extend(auto_apps)

        self.update_settings(INSTALLED_APPS=tuple(installed_apps))
        self.installed_plugins = tuple(plugins)

        if self.override_modlib_models is not None:
            raise Exception("override_modlib_models no longer allowed")

        self.override_modlib_models = dict()
        for p in self.installed_plugins:
                if p.extends_models is not None:
                    for m in p.extends_models:
                        if "." in m:
                            raise Exception(
                                "extends_models in %s still uses '.'" %
                                p.app_name)
                        name = p.extends_from() + '.' + m
                        self.override_modlib_models[name] = p
        # raise Exception("20140825 %s", self.override_modlib_models)

    def is_hidden_app(self, app_label):
        "See :func:`dd.is_hidden_app`."
        am = self.get_apps_modifiers()
        if am.get(app_label, 1) is None:
            return True

    def update_settings(self, **kw):
        """
        This may be called from within a 
        :doc:`djangosite_local.setup_site </djangosite_local>` 
        function.
        """
        self.django_settings.update(**kw)

    def define_settings(self, **kwargs):
        """
        Same as :meth:`update_settings`,        
        but raises an exception if a setting already exists.
        
        TODO: Currently this exception is deactivated.
        Because it doesn't work as expected. 
        For some reason 
        (maybe because settings is being imported twice on a devserver)
        it raises a false exception when 
        :meth:`lino.ui.Site.override_defaults` 
        tries to use it on `MIDDLEWARE_CLASSES`...
        
        """
        if False:
            for name in kwargs.keys():
                if name in self.django_settings:
                    raise Exception(
                        "Tried to define existing Django setting %s" % name)
        self.django_settings.update(kwargs)

    def startup(self):
        "See :func:`dd.startup`."
        
        # This code can run several times at once when running
        # e.g. under mod_wsgi: another thread has started and not yet
        # finished `startup()`.
        if self._startup_done:
            # self.logger.info("20140227 Lino startup already done")
            return

        # self.override_defaults()  # 20140227

        if self._starting_up:
            # raise Exception("Startup called while still starting up.")
            pass
        else:
            self._starting_up = True

            from lino.core.signals import pre_startup, post_startup
            from django.db.models import loading

            pre_startup.send(self)

            for p in self.installed_plugins:
                m = loading.load_app(p.app_name, False)
                self.modules.define(p.app_label, m)

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

    def setup_plugins(self):
        "See :meth:`ad.Site.setup_plugins`."
        pass

    def get_settings_subdirs(self, subdir_name):
        "See :meth:`ad.Site.get_settings_subdirs`."

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

    def makedirs_if_missing(self, dirname):
        "See :func:`dd.makedirs_if_missing`."
        if dirname and not isdir(dirname):
            if self.make_missing_dirs:
                os.makedirs(dirname)
            else:
                raise Exception("Please create yourself directory %s" %
                                dirname)

    def is_installed(self, app_label):
        "See :func:`dd.is_installed`."
        return app_label in self.plugins

    def on_each_app(self, methname, *args):
        "See :func:`dd.on_each_app`."
        from django.db.models import loading
        for mod in loading.get_apps():
            meth = getattr(mod, methname, None)
            if meth is not None:
                meth(self, *args)

    def for_each_app(self, func, *args, **kw):
        "See :func:`dd.for_each_app`."

        from django.utils.importlib import import_module
        done = set()
        for p in self.installed_plugins:
            for b in p.__class__.__mro__:
                if not b in (object, Plugin):
                    if not b.__module__ in done:
                        done.add(b.__module__)
                        parent = import_module(b.__module__)
                        func(b.__module__, parent, *args, **kw)
            if not p.app_name in done:
                func(p.app_name, p.app_module, *args, **kw)

    def demo_date(self, *args, **kwargs):
        "See :attr:`ad.Site.demo_date`."
        base = self.the_demo_date or self.startup_time.date()
        return date_offset(base, *args, **kwargs)

    def today(self):
        return self.the_demo_date or datetime.date.today()

    def welcome_text(self):
        "See :meth:`ad.Site.welcome_text`."
        return "This is %s using %s." % (
            self.site_version(), self.using_text())

    def using_text(self):
        "See :meth:`ad.Site.using_text`."
        return ', '.join(["%s %s" % (n, v)
                          for n, v, u in self.get_used_libs()])

    def site_version(self):
        "See :meth:`ad.Site.site_version`."
        if self.verbose_name:
            assert ispure(self.verbose_name)
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

    def get_default_required(self, **kw):
        #~ if not kw.has_key('auth'):
            #~ kw.update(auth=True)
        if self.user_model is not None:
            kw.setdefault('auth', True)
        return kw

    def parse_date(self, s):
        ymd = tuple(reversed(map(int, s.split('.'))))
        assert len(ymd) == 3
        return ymd
        #~ return datetime.date(*ymd)

    def parse_time(self, s):
        hms = map(int, s.split(':'))
        return datetime.time(*hms)

    def parse_datetime(self, s):
        #~ print "20110701 parse_datetime(%r)" % s
        #~ s2 = s.split()
        s2 = s.split('T')
        if len(s2) != 2:
            raise Exception("Invalid datetime string %r" % s)
        ymd = map(int, s2[0].split('-'))
        hms = map(int, s2[1].split(':'))
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
        "See :meth:`ad.Site.do_site_setup`."
        # self.logger.info("20140227 lino_site.Site.do_site_startup() a")
        
        from lino.core.kernel import Kernel
        self.kernel = Kernel(self)
        self.ui = self.kernel  # internal backwards compat
        self.user_interfaces = tuple([
            p for p in self.installed_plugins
            if isinstance(p, Plugin) and p.ui_label])

        # self.logger.info("20140227 lino_site.Site.do_site_startup() b")

    def find_config_file(self, *args, **kwargs):
        return self.confdirs.find_config_file(*args, **kwargs)

    def find_template_config_files(self, *args, **kwargs):
        return self.confdirs.find_template_config_files(*args, **kwargs)

    def setup_workflows(self):
        self.on_each_app('setup_workflows')

    def setup_choicelists(self):
        #~ raise Exception("20130302 setup_choicelists()")
        #~ logger.info("20130302 setup_choicelists()")
        
        from lino.modlib.users.mixins import UserProfiles, UserGroups

        def grouplevels(level):
            kw = dict(level=level)
            for g in UserGroups.items():
                kw[g.name+'_level'] = level
            return kw

        UserProfiles.reset()
        add = UserProfiles.add_item
        add('000', _("Anonymous"), name='anonymous',
            readonly=self.user_model is not None,
            authenticated=False,
            **grouplevels('user'))
        add('100', _("User"), name='user', **grouplevels('user'))
        add('900', _("Administrator"), name='admin', **grouplevels('admin'))

    def add_user_field(self, name, fld):
        if self.user_model:
            from lino import dd
            #~ User = dd.resolve_model(self.user_model)
            dd.inject_field(self.user_model, name, fld)
            #~ if profile:
                #~ self.user_profile_fields.append(name)

    def get_used_libs(self, html=None):
        "See :meth:`ad.Site.get_used_libs`."
        
        import lino
        yield ("Lino", lino.SETUP_INFO['version'], lino.SETUP_INFO['url'])

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
        """
        This function is called when a Site objects get instantiated,
        i.e. while Django is still loading the settings. It analyzes
        the attribute `languages` and converts it to a tuple of
        `LanguageInfo` objects.
        
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
            if isinstance(self.languages, basestring):
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
            name = to_locale(django_code)
            if name in self.language_dict:
                raise Exception("Duplicate name %s for language code %r"
                                % (name, django_code))
            if i == 0:
                suffix = ''
            else:
                suffix = '_' + name
            info = LanguageInfo(django_code, name, i, str(suffix))
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
        #~ self.BABEL_LANGS = tuple([to_locale(code) for code in self.languages[1:]])
        self.BABEL_LANGS = tuple(self.languages[1:])
        #~ self.AVAILABLE_LANGUAGES = self.AVAILABLE_LANGUAGES + self.BABEL_LANGS

        if must_set_language_code:
            #~ self.update_settings(LANGUAGE_CODE = self.get_default_language())
            self.update_settings(LANGUAGE_CODE=self.languages[0].django_code)
            """
            Note: LANGUAGE_CODE is what *Django* believes to be the default language.
            This should be some variant of English ('en' or 'en-us') 
            if you use `django.contrib.humanize`
            https://code.djangoproject.com/ticket/20059
            """

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
        """Use this in Python fixtures or tests to test whether a 
        Site instance supports a given language. 
        `code` must be a Django-style language code
        If that specified language
        
        On a site with only one locale of a language (and optionally
        some other languages), you can use only the language code to
        get a tuple of `(django_code, babel_locale)`:
        
        >>> from lino.ad import TestSite as Site
        >>> Site(languages="en-us fr de-be de").get_language_info('en')
        LanguageInfo(django_code='en-us', name=u'en_US', index=0, suffix='')
        
        On a site with two locales of a same language (e.g. 'en-us'
        and 'en-gb'), the simple code 'en' yields that first variant:
        
        >>> site = Site(languages="en-us en-gb")
        >>> print site.get_language_info('en')
        LanguageInfo(django_code='en-us', name=u'en_US', index=0, suffix='')

        """
        return self.language_dict.get(code, None)

    def resolve_languages(self, languages):
        """
        This is used by `UserProfile`.
        
        Examples:
        
        >>> from lino.ad import TestSite as Site
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
        if isinstance(languages, basestring):
            languages = languages.split()
        for k in languages:
            if isinstance(k, basestring):
                li = self.get_language_info(k)
                if li is None:
                    raise Exception("Unknown language code %r (must be one of %s)" % (
                        k, [li.name for li in self.languages]))
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
        from django.utils import translation
        for simple, info in self.language_dict.items():
            with translation.override(simple):
                kw[name + info.suffix] = unicode(txt)
        return kw

    def babelkw(self, name, **kw):
        """
        Return a dict with appropriate resolved field names for a
        BabelField `name` and a set of hard-coded values.

        You have some hard-coded multilingual content in a fixture:

        >>> from lino.ad import TestSite as Site
        >>> kw = dict(de="Hallo", en="Hello", fr="Salut")

        The field names where this info gets stored depends on the
        Site's `languages` distribution.
        
        >>> Site(languages="de-be en").babelkw('name',**kw)
        {'name_en': 'Hello', 'name': 'Hallo'}
        
        >>> Site(languages="en de-be").babelkw('name',**kw)
        {'name_de_BE': 'Hallo', 'name': 'Hello'}
        
        >>> Site(languages="en-gb de").babelkw('name',**kw)
        {'name_de': 'Hallo', 'name': 'Hello'}
        
        >>> Site(languages="en").babelkw('name',**kw)
        {'name': 'Hello'}
        
        >>> Site(languages="de-be en").babelkw('name',de="Hallo",en="Hello")
        {'name_en': 'Hello', 'name': 'Hallo'}

        In the following example `babelkw` attributes the 
        keyword `de` to the *first* language variant:
        
        >>> Site(languages="de-ch de-be").babelkw('name',**kw)
        {'name': 'Hallo'}
        
        
        """
        d = dict()
        for simple, info in self.language_dict.items():
            v = kw.get(simple, None)
            if v is not None:
                d[name + info.suffix] = v
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
        #~ d = { self.DEFAULT_LANGUAGE.name : getattr(obj,name) }
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
        from django.utils import translation
        if len(args) == 0:
            info = self.language_dict.get(
                translation.get_language(), self.DEFAULT_LANGUAGE)
            default_value = None
            if info == self.DEFAULT_LANGUAGE:
                return values.get(info.name)
            x = values.get(info.name, None)
            if x is None:
                return values.get(self.DEFAULT_LANGUAGE.name)
            return x
        elif len(args) == 1:
            info = self.language_dict.get(translation.get_language(), None)
            if info is None:
                return args[0]
            default_value = args[0]
            return values.get(info.name, default_value)
        raise ValueError("%(values)s is more than 1 default value." %
                         dict(values=args))

    # babel_get(v) = babelitem(**v)

    def babeldict_getitem(self, d, k):
        v = d.get(k, None)
        if v is not None:
            assert type(v) is dict
            return self.babelitem(**v)

    def babelattr(self, obj, attrname, default=NOT_PROVIDED, language=None):
        if language is None:
            from django.utils import translation
            language = translation.get_language()
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

    def diagnostic_report_rst(self):

        s = ''
        s += "plugins: %s\n" % repr(self.plugins)
        for k, p in self.plugins.items():
            s += "%s : %s\n" % (k, p)
        # s += "config_dirs: %s\n" % repr(self.confdirs.config_dirs)
        s += "\n"
        for cd in self.confdirs.config_dirs:
            ln = relpath(cd.name)
            if cd.writeable:
                ln += " [writeable]"
            s += ln + '\n'
        return s

    def get_db_overview_rst(self):
        from atelier import rstgen
        from lino.core.dbutils import (full_model_name,
                                       sorted_models_list, app_labels)

        #~ writeln("Lino %s" % lino.__version__)
        #~ yield (settings.SITE.verbose_name, settings.SITE.version)
        #~ writeln(settings.SITE.title)
        models_list = sorted_models_list()
        apps = app_labels()
        s = "%d apps: %s." % (len(apps), ", ".join(apps))
        s += "\n%d models:\n" % len(models_list)
        i = 0
        headers = [
            #~ "No.",
            "Name",
            #~ "Class",
            #~ "M",
            "#fields",
            "#rows",
            #~ ,"first","last"
        ]
        rows = []
        for model in models_list:
            if model._meta.managed:
                i += 1
                cells = []
                #~ cells.append(str(i))
                cells.append(full_model_name(model))
                #~ cells.append(str(model))
                #~ if model._meta.managed:
                #~ cells.append('X')
                #~ else:
                #~ cells.append('')
                cells.append(str(len(model._meta.fields)))
                #~ qs = model.objects.all()
                qs = model.objects.order_by('pk')
                n = qs.count()
                cells.append(str(n))
                #~ if n:
                #~ cells.append(obj2str(qs[0]))
                #~ cells.append(obj2str(qs[n-1]))
                #~ else:
                #~ cells.append('')
                #~ cells.append('')

                rows.append(cells)
        s += rstgen.table(headers, rows)
        return s

    def override_defaults(self, **kwargs):
        """
        Called internally during `__init__` method.
        Also called from :mod:`lino.utils.djangotest`

        """
        #~ logger.info("20130404 lino.site.Site.override_defaults")

        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self.__class__, k))
            setattr(self, k, v)

        self.apply_languages()

        if self.webdav_url is None:
            self.webdav_url = '/media/webdav/'
        if self.webdav_root is None:
            self.webdav_root = join(
                abspath(self.project_dir), 'media', 'webdav')

        if not self.django_settings.get('MEDIA_ROOT', False):
            """
            Django's default value for MEDIA_ROOT is an empty string.
            In certain test cases there migth be no MEDIA_ROOT key at all.
            Lino's default value for MEDIA_ROOT is ``<project_dir>/media``.
            """
            self.django_settings.update(
                MEDIA_ROOT=join(self.project_dir, 'media'))

        self.update_settings(
            ROOT_URLCONF='lino.ui.urls'
        )
        self.update_settings(
            MEDIA_URL='/media/'
        )
        self.update_settings(
            TEMPLATE_LOADERS=tuple([
                'lino.core.web.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                #~ 'django.template.loaders.eggs.Loader',
            ]))

        tcp = []
        if self.user_model == 'auth.User':
            self.update_settings(LOGIN_URL='/accounts/login/')
            self.update_settings(LOGIN_REDIRECT_URL="/")
            tcp += ['django.contrib.auth.context_processors.auth']

        tcp += [
            'django.core.context_processors.debug',
            'django.core.context_processors.i18n',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            #    'django.core.context_processors.request',
            #~ 'django.contrib.messages.context_processors.messages',
        ]
        self.update_settings(TEMPLATE_CONTEXT_PROCESSORS=tuple(tcp))

        self.define_settings(
            MIDDLEWARE_CLASSES=tuple(self.get_middleware_classes()))

        #~ print 20130313, self.django_settings['MIDDLEWARE_CLASSES']

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

        if not 'system' in self.modules:
            return None

        if self._site_config is None:
            #~ raise Exception(20130301)
            #~ print '20130320 create _site_config'
            #~ from lino.core.dbutils import resolve_model
            #~ from lino.core.dbutils import obj2str
            #~ from lino.utils import dblogger as logger
            #~ SiteConfig = resolve_model('system.SiteConfig')
            SiteConfig = self.modules.system.SiteConfig
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
        from django.utils.translation import ugettext_lazy as _
        from lino.core import menus
        main = menus.Toolbar(profile, 'main')
        self.setup_menu(ui, profile, main)
        main.compress()
        #~ url = self.admin_url
        #~ if not url:
            #~ url = "/"
        #~ main.add_url_button(url,label=_("Home"))
        #~ url = "javascript:Lino.close_all_windows()"
        #~ main.add_url_button(url,label=_("Home"))
        return main

    def setup_quicklinks(self, ar, m):
        """
        Override this
        in application-specific (or even local) :xfile:`settings.py` files
        to define a series of *quick links* to appear below the main menu bar.
        Example see :meth:`lino.projects.pcsw.settings.Site.setup_quicklinks`.
        """
        self.on_each_app('setup_quicklinks', ar, m)

    def setup_menu(self, ui, profile, main):
        """
        Set up the application's menu structure.

        The default implementation uses a system of
        predefined top-level items that are filled by the
        different :setting:`INSTALLED_APPS`.
        To use this system, application programmers
        define one or several of the following functions in
        their `models` module:

        - `setup_master_menu`
        - `setup_main_menu`
        - `setup_reports_menu`
        - `setup_config_menu`
        - `setup_explorer_menu`
        - `setup_site_menu`

        These functions, if present, will be called with three
        positional arguments: `ui`, `profile` and `menu`.
        The first argument `ui` should not be used.
        TODO: remove that argument from API.

        """
        from django.utils.translation import ugettext_lazy as _
        m = main.add_menu("master", _("Master"))
        self.on_each_app('setup_master_menu', ui, profile, m)
        #~ if not profile.readonly:
            #~ m = main.add_menu("my",_("My menu"))
            #~ self.on_each_app('setup_my_menu',ui,profile,m)
        self.on_each_app('setup_main_menu', ui, profile, main)
        m = main.add_menu("reports", _("Reports"))
        self.on_each_app('setup_reports_menu', ui, profile, m)
        m = main.add_menu("config", _("Configure"))
        self.on_each_app('setup_config_menu', ui, profile, m)
        m = main.add_menu("explorer", _("Explorer"))
        self.on_each_app('setup_explorer_menu', ui, profile, m)
        m = main.add_menu("site", _("Site"))
        self.on_each_app('setup_site_menu', ui, profile, m)
        return main

    def get_middleware_classes(self):
        """
        Yields the strings to be stored in
        the :setting:`MIDDLEWARE_CLASSES` setting.

        In case you don't want to use this method
        for defining :setting:`MIDDLEWARE_CLASSES`,
        you can simply set :setting:`MIDDLEWARE_CLASSES`
        in your :xfile:`settings.py`
        after the :class:`lino.site.Site` has been instantiated.

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
        #~ elif self.remote_user_header:

        if self.auth_middleware:
            yield self.auth_middleware
        else:
            if self.user_model is None:
                yield 'lino.core.auth.NoUserMiddleware'
            elif self.remote_user_header:
                yield 'lino.core.auth.RemoteUserMiddleware'
                #~ yield 'django.middleware.doc.XViewMiddleware'
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

    def get_main_action(self, profile):
        """
        Return the action to show as top-level "index.html".
        The default implementation returns `None`, which means
        that Lino will call :meth:`get_main_html`.
        """
        return None

    def get_main_html(self, request):
        """Return a chunk of html to be displayed in the main area of the
        admin index.  This is being called only if
        :meth:`get_main_action` returns `None`.  The default
        implementation renders the :xfile:`admin_main.html` template.

        """
        from lino.core import web
        return web.render_from_request(request, 'admin_main.html')

    def get_welcome_messages(self, ar):
        for a in self._welcome_actors:
            for msg in a.get_welcome_messages(ar):
                yield msg

    def get_installed_apps(self):
        "See :meth:`dd.Site.get_installed_apps`."

        if self.user_model is not None and self.remote_user_header is None:
            yield 'django.contrib.sessions'  # 20121103
        if self.django_admin_prefix:
            yield 'django.contrib.admin'
        yield 'lino.modlib.about'
        yield 'lino.modlib.extjs'
        yield 'lino.modlib.bootstrap3'
        for a in self.user_apps:
            yield a
        yield "lino"

    site_prefix = '/'

    def buildurl(self, *args, **kw):
        #~ url = '/' + ("/".join(args))
        url = self.site_prefix + ("/".join(args))
        if len(kw):
            url += "?" + urlencode(kw)
        return url

    def build_media_url(self, *args, **kw):
        return self.buildurl('media', *args, **kw)

    def build_admin_url(self, *args, **kw):
        # backwards compatibility
        return self.kernel.default_renderer.plugin.build_plain_url(
            *args, **kw)
        
    def build_extjs_url(self, *args, **kw):
        # backwards compatibility
        return self.kernel.default_renderer.plugin.build_media_url(
            *args, **kw)

    def build_tinymce_url(self, url):
        if self.tinymce_base_url:
            return self.tinymce_base_url + url
        return self.build_media_url('tinymce', url)

    def get_system_note_recipients(self, ar, obj, silent):
        "See :meth:`ad.Site.get_system_note_recipients`."
        return obj.get_system_note_recipients(ar, silent)

    def welcome_html(self, ui=None):
        "See :meth:`ad.Site.welcome_html`."
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
        "See :func:`rt.login`."
        self.startup()
        if self.user_model is None or username is None:
            if not 'user' in kw:
                from lino.core.auth import AnonymousUser
                kw.update(user=AnonymousUser.instance())
        else:
            kw.update(user=self.user_model.objects.get(username=username))

        if not 'renderer' in kw:
            kw.update(renderer=self.ui.text_renderer)

        from lino.core import requests
        import lino.ui.urls  # hack: trigger ui instantiation
        return requests.BaseRequest(**kw)

    def get_letter_date_text(self, today=None):
        "See :meth:`ad.Site.get_letter_date_text`."
        sc = self.site_config.site_company
        if today is None:
            today = self.today()
        from lino.utils.format_date import fdl
        if sc and sc.city:
            return _("%(place)s, %(date)s") % dict(
                place=unicode(sc.city.name), date=fdl(today))
        return fdl(today)

    def get_admin_main_items(self):
        "See :func:`ad.Site.get_admin_main_items`."
        return []

    def make_cache_file(self, fn, write, force=False):

        if not force and os.path.exists(fn):
            mtime = os.stat(fn).st_mtime
            if mtime > self.kernel.code_mtime:
                # logger.info(
                #     "20140401 %s (%s) is up to date.", fn, time.ctime(mtime))
                return 0

        self.logger.info("Building %s ...", fn)
        self.makedirs_if_missing(os.path.dirname(fn))
        f = codecs.open(fn, 'w', encoding='utf-8')
        try:
            write(f)
            f.close()
            return 1
        except Exception:
            """
            If some error occurs, remove the partly generated file
            to make sure that Lino will try to generate it again
            (and report the same error message) on next request.
            """
            f.close()
            #~ os.remove(fn)
            raise
        #~ logger.info("Wrote %s ...", fn)

    def decfmt(self, v, places=2, **kw):
        """
        Format a Decimal value.
        Like :func:`lino.utils.moneyfmt`, but using the site settings
        :attr:`lino.Lino.decimal_group_separator`
        and
        :attr:`lino.Lino.decimal_separator`.
        """
        kw.setdefault('sep', self.decimal_group_separator)
        kw.setdefault('dp', self.decimal_separator)
        from lino.utils import moneyfmt
        return moneyfmt(v, places=places, **kw)

    def get_printable_context(self, **kw):
        from django.conf import settings
        from django.utils.translation import ugettext_lazy as _
        from lino import dd, rt
        from lino.utils import iif

        kw.update(
            dtos=dd.fds,  # obsolete
            dtosl=dd.fdf,  # obsolete
            dtomy=dd.fdmy,  # obsolete
            mtos=self.decfmt,  # obsolete
            decfmt=self.decfmt,
            fds=dd.fds,
            fdm=dd.fdm,
            fdl=dd.fdl,
            fdf=dd.fdf,
            fdmy=dd.fdmy,
            babelattr=dd.babelattr,
            babelitem=self.babelitem,
            tr=self.babelitem,
            iif=iif,
            dd=dd,
            rt=rt,
            settings=settings,
            lino=self.modules,  # experimental
            site_config=self.site_config,
        )

        def translate(s):
            return _(s.decode('utf8'))
        kw.update(_=translate)
        return kw

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
        if p.startswith(self.project_dir):
            p = "$(PRJ)" + p[len(self.project_dir):]
        return p


class TestSite(Site):

    """Used to simplify doctest strings because it inserts default values
    for the two first arguments that are mandatory but not used in our
    examples::
    
    >> from lino.ad import Site
    >> Site(globals(), ...)
    
    >> from lino.ad import TestSite as Site
    >> Site(...)

    """

    def __init__(self, *args, **kwargs):
        kwargs.update(no_local=True)
        g = dict(__file__=__file__)
        g.update(SECRET_KEY="20227")  # see :djangoticket:`20227`
        super(TestSite, self).__init__(g, *args, **kwargs)

        # 20140913 Hack needed for doctests in :mod:`ad`.
        from django.utils import translation
        translation._default = None


