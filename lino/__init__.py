# -*- coding: UTF-8 -*-
## Copyright 2002-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

"""
The ``lino`` module can be imported even from a Django :xfile:`settings.py` 
file since it does not import any django module.

"""

import os
import sys
import cgi
import inspect
import datetime

from os.path import join, abspath, dirname, normpath, isdir
from decimal import Decimal

from .utils.xmlgen import html as xghtml
from .utils import AttrDict

execfile(os.path.join(os.path.dirname(__file__),'version.py'))

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

#~ __url__ = "http://lino.saffre-rumma.net"
#~ __url__ = "http://code.google.com/p/lino/"
__url__ = "http://www.lino-framework.org"


__copyright__ = """\
Copyright (c) 2002-2013 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""

gettext = lambda s: s

def language_choices(*args):
    """
    A subset of Django's LANGUAGES.
    See :doc:`/blog/2011/0226`.
    """
    _langs = dict(
        en=gettext('English'),
        de=gettext('German'),
        fr=gettext('French'),
        nl=gettext('Dutch'),
        et=gettext('Estonian'),
    )
    return [(x,_langs[x]) for x in args]
      



if False: 
    """
    subprocess.Popen() took very long and even got stuck on Windows XP.
    I didn't yet explore this phenomen more.
    """
    # Copied from Sphinx <http://sphinx.pocoo.org>
    from os import path
    package_dir = path.abspath(path.dirname(__file__))
    if '+' in __version__ or 'pre' in __version__:
        # try to find out the changeset hash if checked out from hg, and append
        # it to __version__ (since we use this value from setup.py, it gets
        # automatically propagated to an installed copy as well)
        try:
            import subprocess
            p = subprocess.Popen(['hg', 'id', '-i', '-R',
                                  path.join(package_dir, '..', '..')],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if out:
                __version__ += ' (Hg ' + out.strip() +')'
            #~ if err:
                #~ print err
        except Exception:
            pass


NOT_FOUND_MSG = '(not installed)'

STARTUP_DONE = False

class Lino(object):
    """
    Base class for the Lino instance stored in :setting:`LINO`.
    Lino applications add one setting `LINO` 
    which is an instance of the :class:`lino.Lino` class.
    This simple trick brings inheritance to the settings and lets us define 
    methods.
    
    This class is first defined in :mod:`lino`, 
    then usually subclassed by the application developer
    (e.g. :mod:`lino.apps.cosi.Lino`),
    then imported into your local :xfile:`settings.py`,
    where you may subclass it another time before 
    finally instantiating it, and assigning it to 
    the :setting:`LINO` variable.
    
    Instiatiation is always the same line of code::
    
      LINO = Lino(__file__,globals())
      
    With the parameters `__file__` and `globals()` you give Lino 
    information about your local settings (where they are in the file 
    system), and the possibility to modify your Django settings.
    
    Lino will modify the following Django settings 
    (which means that if you want to modify one of these, 
    do it *after* instantiating your :setting:`LINO`):
    
      :setting:`ROOT_URLCONF`
      :setting:`SERIALIZATION_MODULES`
      :setting:`MEDIA_ROOT` 
      :setting:`TEMPLATE_DIRS`
      :setting:`FIXTURE_DIRS` 
      :setting:`LOGGING_CONFIG`
      :setting:`LOGGING`
      :setting:`MIDDLEWARE_CLASSES`
      :setting:`TEMPLATE_LOADERS`
      ...
    
    """
    
    partners_app_label = 'contacts'
    """
    Temporary setting, see :doc:`/tickets/72`
    """
    
    # three constants used by lino.modlib.workflows:
    max_state_value_length = 20 
    max_action_name_length = 50
    max_actor_name_length = 100
    
    allow_duplicate_cities = False
    """
    In a default configuration (when :attr:`allow_duplicate_cities` is False), 
    Lino declares a UNIQUE clause 
    for :class:`Cities <lino.modlib.countries.models.Cities>` 
    to make sure that your database never contains duplicate cities.
    This behaviour mighr disturb e.g. when importing legacy data that 
    did not have this restriction.
    Set it to True to remove the UNIQUE clause.
    
    Changing this setting might affect your database structure 
    and thus require a :doc:`/topics/datamig`
    if your application uses :mod:`lino.modlib.countries`.
    
    """
    
    
    help_url = "http://code.google.com/p/lino"
    #~ site_url = 
    #~ index_html = "This is the main page."
    title = None
    #~ domain = "www.example.com"
    
    short_name = None # "Unnamed Lino Application"
    """
    Used as display name to end-users at different places.
    """
    
    author = None
    author_email = None
    version = None
    """
    """
    
    url = None
    """
    """
    
    description = """yet another <a href="%s">Lino</a> application.""" % __url__
    """
    A short single-sentence description.
    It should start with a lowercase letter because the beginning 
    of the sentence will be generated from other class attributes 
    like :attr:`short_name` and :attr:`version`.
    """
    
    uid = 'myuid'
    """
    A universal identifier for this Lino site. 
    This is needed when synchronizing with CalDAV server.  
    Locally created calendar components in remote calendars 
    will get a UID based on this parameter,
    using ``"%s@%s" (self.pk,settings.LINO.ui)``.
    
    The default value is ``'myuid'``, and
    you should certainly override this 
    on a production server that uses remote calendars.
    """
    
    #~ person_model = None
    #~ person_model = "contacts.Person"
    #~ """
    #~ If your application uses :model:`lino.modlib.contacts`,
    #~ set this to a string "applabel.Modelname" which identifies 
    #~ your Person model (which should inherit from
    #~ :class:`lino.modlib.contacts.models.Person`).
    #~ """
    
    #~ company_model = None
    #~ company_model = "contacts.Company"
    #~ """
    #~ If your application uses :model:`lino.modlib.contacts`,
    #~ set this to a string "applabel.Modelname" which identifies 
    #~ your Company model (which should inherit from
    #~ :class:`lino.modlib.contacts.models.Company`).
    #~ """
    
    project_model = None
    """
    Optionally set this to the <applabel_modelname> of a 
    model used as project in your application.
    """
    
    #~ user_model = "users.User"
    user_model = None
    """
    Set this to ``"auth.User"`` if you use `django.contrib.auth` instead of
    `lino.modlib.users`. 
    
    Set it to `None` to remove any user management 
    (feature used by e.g. :mod:`lino.test_apps.1`)
    """
    
    is_local_project_dir = False
    """
    This is automatically set when a :class:`Lino` is instantiated. 
    Don't override it.
    Contains `True` if this is a "local" project.
    For local projects, Lino checks for local fixtures and config directories
    and adds them to the default settings.
    """
    
    
    legacy_data_path = None
    """
    Used by custom fixtures that import data from some legacy database.    
    """
    
    migration_module = None
    """If you maintain a data migration module for your application, 
    specify its name here."""
   
    
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
    
    make_missing_dirs = True
    """
    Set this to False if you don't want Lino to automatically 
    create missing dirs when needed 
    (but to raise an exception in these cases, asking you to create it yourself)
    """
    
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
    
    
    #~ preferred_build_method = 'pisa'
    #~ preferred_build_method = 'appypdf'
    
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
    
    propvalue_max_length = 200
    """
    Used by :mod:`lino.modlib.properties`.
    """
    
    appy_params = dict(ooPort=8100)
    """
    Used by :class:`lino.mixins.printable.AppyBuildMethod`.
    """
    
    #~ source_dir = None # os.path.dirname(__file__)
    #~ """
    #~ Full path to the source directory of this Lino application.
    #~ Local Lino subclasses should not override this variable.
    #~ This is used in :mod:`lino.utils.config` to decide 
    #~ whether there is a local config directory.
    #~ """
    
    #~ source_name = None  # os.path.split(source_dir)[-1]
    
    project_name = None
    """
    Read-only.
    The leaf name of your local project directory.
    """
    
    project_dir = None
    """
    Read-only.
    Full path to your local project directory. 
    Local Lino subclasses should not override this variable.
    
    The local project directory is where 
    local configuration files are stored:
    
    - Your :xfile:`settings.py`
    - Optionally the :xfile:`manage.py` and :xfile:`urls.py` files
    - Your :xfile:`media` directory
    - Optional local :xfile:`config` and :xfile:`fixtures` directories
    """
    
    loading_from_dump = False
    """
    Set to `False` by python dumps that were generated by
    :meth:`lino.utils.dumpy.Serializer.serialize`.
    Used in 
    :func:`lino.modlib.cal.models.update_auto_task`
    and
    :mod:`lino.modlib.mails.models`.
    See also :doc:`/blog/2011/0901`.
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
    """
    Format (in strftime syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.
    """
    
    time_format_extjs = 'H:i'
    """
    Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.
    """
    
    date_format_strftime = '%d.%m.%Y'
    """
    Format (in strftime syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.
    """
    
    date_format_extjs = 'd.m.Y'
    """
    Format (in ExtJS syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.
    """
    
    alt_date_formats_extjs = 'd/m/Y|Y-m-d'
    """
    Alternative date entry formats accepted by ExtJS Date widgets.
    """
    
    #~ date_format_regex = "/^[0123]\d\.[01]\d\.-?\d+$/"
    date_format_regex = "/^[0123]?\d\.[01]?\d\.-?\d+$/"
    """
    Format (in Javascript regex syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.
    """
    
    datetime_format_strftime = '%Y-%m-%dT%H:%M:%S'
    """
    Format (in strftime syntax) to use for formatting timestamps in AJAX responses.
    If you change this setting, you also need to override :meth:`parse_datetime`.
    """
    
    datetime_format_extjs = 'Y-m-d\TH:i:s'
    """
    Format (in ExtJS syntax) to use for formatting timestamps in AJAX calls.
    If you change this setting, you also need to override :meth:`parse_datetime`.
    """
    
    #~ default_number_format_extjs = '0,000.00/i'
    default_number_format_extjs = '0,00/i'
    
    uppercase_last_name = False
    """
    Whether last name of persons should be printed with uppercase letters.
    See :mod:`lino.test_apps.human`
    """
    
    cbss_live_tests = False
    """
    Whether unit tests should try to really connect to the cbss.
    Some test cases of the test suite would fail with a timeout if run 
    from behind an IP address that is not registered at the :term:`CBSS`.
    These tests are skipped by default. To activate them, 
    set `cbss_live_tests` to `True` in your :xfile:`settings.py`.
    
    """
    
    cbss_environment = None
    """
    Either `None` or one of 'test', 'acpt' or 'prod'.
    See :mod:`lino.modlib.cbss.models`.
    Leaving this to `None` means that the cbss module is "inactive" even if installed.
    """
    
    languages = ['en']
    """
    The language distribution used in this database.
    
    This must be an iterable of 2-letter codes.
    Examples::
    
      languages = "en de fr nl et".split()
      languages = ['en']
      
    The first language in this list will be the site's 
    default language.
    
    Changing this setting might affect your database structure 
    and thus require a :doc:`/topics/datamig`
    if your application uses :doc:`/topics/babel`.    
    
    Lino will use this setting to set the Django 
    settings :setting:`LANGUAGES` and  :setting:`LANGUAGE_CODE`.
    
    """
    
    site_config = None
    """
    ui.Lino overrides this to hold a SiteConfig instance.
    """
    
    max_auto_events = 36
    """
    Maximum number of automatic events to be generated 
    by :class:`lino.modlib.cal.models.EventOwner`.
    """
    
    #~ mergeable_models = []
    #~ """
    #~ A list of models that should have a "Merge" action
    #~ (see :mod:`lino.mixins.mergeable`).
    #~ """
    
    override_modlib_models = []
    """
    A list of names of modlib models which are being 
    redefined by this application.
    
    The following modlib models currently support this:
    - :class:`contacts.Person <lino.modlib.contacts.models.Person>`
    - :class:`contacts.Company <lino.modlib.contacts.models.Company>`
    
    Usage: in your application's `settings.py`, specify::
    
      class Lino(Lino):
          override_modlib_models = ['contacts.Person']
          
    This will cause the modlib Person model to be abstract, 
    and hence your application is responsible for defining another 
    `Person` class with "contacts" as `app_label`::
          
      class Person(contacts.Person,mixins.Born):
          class Meta(contacts.Person.Meta):
              app_label = 'contacts'
              
          def kiss(self):
              ...
    
    """
    
    modules = AttrDict()
    """
    A shortcut to access all installed models and actors.
    Read-only. Applications should not set this. 
    """
    
    django_settings = None
    """
    This is where Lino stores the `globals()` dictionary of your
    :xfile:`settings.py` file (the one you provided when 
    calling :meth:`Lino.__init__`.
    """
    
    
    demo_fixtures = ['std','demo']
    """
    The list of fixtures to be loaded by the 
    `initdb_demo <lino.management.commands.initdb_demo>`
    command.
    """
    
    
    #~ use_contenttypes = True
    #~ """
    #~ Set this to False if you don't want to use `django.contrib.contenttypes`.
    #~ """
    
    #~ index_view_action = 'lino.Home'
    
    
    
    def __init__(self,project_file,django_settings):
      
        #~ self.user_profile_fields = ['level']
        
        #~ self.version = __version__
        
        #~ self._watch_changes_requests = []
        
        #~ print 20130219, __file__, self.__class__
        
        self.project_dir = normpath(dirname(project_file))
        self.project_name = os.path.split(self.project_dir)[-1]
        
        
        self.qooxdoo_prefix = '/media/qooxdoo/lino_apps/' + self.project_name + '/build/'
        #~ self.dummy_messages = set()
        #~ self._starting_up = False
        #~ self._startup_done = False
        #~ self._response = None
        self.django_settings = django_settings
        self.GFK_LIST = []
        
        
        django_settings.update(
            LOGGING_CONFIG='lino.utils.log.configure',
            LOGGING=dict(filename=None,level='INFO'),
            )
        
        django_settings.update(SERIALIZATION_MODULES = {
            "py" : "lino.utils.dumpy",
        })
        
        self.startup_time = datetime.datetime.now()
        
        if self.languages:
            lc = language_choices(*self.languages)
            django_settings.update(LANGUAGES = lc)
            django_settings.update(LANGUAGE_CODE = lc[0][0])
        
        try:
            from lino_local import on_init
            #~ from sitecustomize_lino import on_init
            #~ import sitecustomize_lino
            #~ raise Exception("""
            #~ Replace your sitecustomize_lino module 
            #~ (%s)
            #~ by a LocalLinoMixin
            #~ as documented in 
            #~ http://lino-framework.org/admin/local_lino.html
            #~ """ % sitecustomize_lino.__file__)
        except ImportError:
            pass
        else:
            on_init(self)
        
        #~ s.update(DATABASES= {
              #~ 'default': {
                  #~ 'ENGINE': 'django.db.backends.sqlite3',
                  #~ 'NAME': join(LINO.project_dir,'test.db')
              #~ }
            #~ })
        
    def get_settings_subdirs(self,subdir_name):
        """
        Yield all (existing) directories named `subdir_name` 
        of this site's project directory and it's inherited 
        project directories.
        """
        for cl in self.__class__.__mro__:
            #~ logger.info("20130109 inspecting class %s",cl)
            if cl is not object and not inspect.isbuiltin(cl):
                pth = join(dirname(inspect.getfile(cl)),subdir_name)
                if isdir(pth):
                    yield pth
          
       
    def is_abstract_model(self,name):
        return name in self.override_modlib_models
        
    def parse_date(self,s):
        """Convert a string formatted using 
        :attr:`date_format_strftime` or  :attr:`date_format_extjs` 
        into a `(y,m,d)` tuple (not a `datetime.date` instance).
        See :doc:`/blog/2010/1130`.
        """
        ymd = tuple(reversed(map(int,s.split('.'))))
        assert len(ymd) == 3
        return ymd
        #~ return datetime.date(*ymd)
        
    def parse_time(self,s):
        """Convert a string formatted using 
        :attr:`time_format_strftime` or  :attr:`time_format_extjs` 
        into a datetime.time instance.
        """
        hms = map(int,s.split(':'))
        return datetime.time(*hms)
        
    def parse_datetime(self,s):
        """Convert a string formatted using
        :attr:`datetime_format_strftime` or  :attr:`datetime_format_extjs` 
        into a datetime.datetime instance.
        """
        #~ print "20110701 parse_datetime(%r)" % s
        #~ s2 = s.split()
        s2 = s.split('T')
        if len(s2) != 2:
            raise Exception("Invalid datetime string %r" % s)
        ymd = map(int,s2[0].split('-'))
        hms = map(int,s2[1].split(':'))
        return datetime.datetime(*(ymd+hms))
        #~ d = datetime.date(*self.parse_date(s[0]))
        #~ return datetime.combine(d,t)

    
    #~ def get_user_model(self):
        #~ if 'django.contrib.auth' in self.django_settings['INSTALLED_APPS']:
            #~ from django.contrib.auth.models import User
            #~ return 'auth.User'
        #~ else:
            #~ from lino.modlib.users.models import User
        #~ return User
        #~ return 'users.User'
      
        

    #~ def add_dummy_message(self,s):
        #~ self.dummy_messages.add(s)

    #~ def get_app_source_file(self):
        #~ "Override this in each application"
        #~ return __file__
        
    def is_imported_partner(self,obj):
        """
        Return whether the specified
        :class:`Partner <lino.modlib.contacts.models.Partner>` instance
        `obj` is to be considered as imported from some legacy database.
        """
        #~ return obj.id is not None and (obj.id < 200000 or obj.id > 299999)
        return False
        #~ return obj.id is not None and (obj.id > 10 and obj.id < 21)
                  
        
    #~ def analyze_models(self):
        #~ from lino.core.kernel import analyze_models
        #~ analyze_models()
        
    def startup(self,**options):
        """
        Start the Lino instance (the object stored as :setting:`LINO` in your :xfile:`settings.py`).
        This is called exactly once from :mod:`lino.models` 
        when Django has has populated it's model cache.
        
        This can happen when running e.g. under mod_wsgi: 
        another thread has started and not yet finished `startup_site()`, 
        so keep your fingers away and don't start a second time.
        
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info("Lino startup (PID %s)",os.getpid())
        
        global STARTUP_DONE
        if STARTUP_DONE: 
            #~ print "20130219 DONE"
            logger.info("Lino startup already done")
            return
        STARTUP_DONE = True
        
        #~ if self._startup_done:
            #~ # logger.warning("LinoSite setup already done ?!")
            #~ return
            
        #~ logger.info("startup_site()")
        
        from lino.core.kernel import startup_site
        startup_site(self,**options)
        
        #~ import time

        #~ import threading
        #~ write_lock = threading.RLock()
        #~ write_lock = threading.Lock()
        
        #~ write_lock.acquire()
        
        #~ if self._starting_up:
            #~ while self._starting_up:
                #~ logger.warning("Lino.startup() waiting...")
                #~ time.sleep(1)
            #~ return 
            
        #~ if self._starting_up:
            #~ # logger.warning("Lino.startup() called recursively.")
            #~ """
            #~ This can happen when running e.g. under mod_wsgi: 
            #~ another thread has started the work, so keep your fingers 
            #~ away and don't start a second time.
            #~ """
            #~ # write_lock.release()
            #~ # return 
            #~ raise Exception("Lino.startup() called recursively.")
            
        #~ self._starting_up = True
        
        
        #~ try:
          
            #~ startup_site(self,**options)
        
            #~ self._startup_done = True
        #~ finally:
            #~ self._starting_up = False
            #~ write_lock.release()
        
    def setup_workflows(self):
        self.on_each_app('setup_workflows')
        
    def setup_choicelists(self):
        """
        Redefine application-specific Choice Lists.
        
        Especially used to define application-specific
        :class:`UserProfiles <lino.core.perms.UserProfiles>`.
        
        Lino by default has two user profiles "User" 
        and "Administrator", defined in :mod:`lino.core.perms`.
        
        Application developers who use group-based requirements 
        must override this in their application's :xfile:`settings.py` 
        to provide a default list of user profiles for their 
        application.
        
        See the source code of :mod:`lino.apps.presto` 
        or :mod:`lino.apps.pcsw` for a usage example.
        
        Local site administrators may again override this in their 
        :xfile:`settings.py`.
        
        Note that you may not specify values longer 
        than `max_length` when redefining your choicelists.
        This limitation is because these redefinitions happen at a 
        moment where database fields have already been instantiated, 
        so it is too late to change their max_length.        
        Not that this limitation is only for the *values*, not for the names 
        or texts of choices.
        
        """
        
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset()
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"), name='anonymous', level=None,
            #~ readonly=True,
            authenticated=False)
        add('100', _("User"), name='user', level='user')
        add('900', _("Administrator"), name='admin', level='admin')
        
        
        
    def add_user_field(self,name,fld):
        if self.user_model:
            from lino import dd
            #~ User = dd.resolve_model(self.user_model)            
            dd.inject_field(self.user_model,name,fld)
            #~ if profile:
                #~ self.user_profile_fields.append(name)

    def is_installed(self,app_label):
        """
        Return `True` if :setting:`INSTALLED_APPS` contains an item
        which ends with the specified `app_label`.
        """
        from django.conf import settings
        #~ if not '.' in app_label:
            #~ app_label = '.' + app_label
        for s in settings.INSTALLED_APPS:
            if s == app_label or s.endswith('.'+app_label):
            #~ if s.endswith(app_label):
                return True
        #~ print "20120703 not installed: %r" % app_label


    def get_installed_modules(self):
        from django.conf import settings
        from django.utils.importlib import import_module
        for app_name in settings.INSTALLED_APPS:
            yield import_module('.models', app_name)
        
    def on_each_app(self,methname,*args):
        """
        Call the named method on each module in :setting:`INSTALLED_APPS`
        that defines it.
        """
        from lino.utils import dblogger
        for mod in self.get_installed_modules():
            meth = getattr(mod,methname,None)
            if meth is not None:
                #~ dblogger.debug("Running %s of %s", methname, mod.__name__)
                meth(self,*args)
        
        
    #~ def get_calendar_color(self,calendar,request):
        #~ if calendar.user == request.user:
            #~ return 5
        #~ return 2
        
    def demo_date(self,days=0,**offset):
        """
        Used e.g. in python fixtures.
        """
        if days:
            offset.update(days=days)
        #~ J = datetime.date(2011,12,16)
        if offset:
            return self.startup_time.date() + datetime.timedelta(**offset)
        return self.startup_time.date()
        
        
    vat_quarterly = False
    """
    Set this to True to support quarterly VAT declarations.
    """
    
    def get_vat_class(self,tt,item):
        return 'normal'
        
    def get_product_vat_class(self,tt,product):
        return 'normal'
        

    def get_product_base_account(self,tt,product):
        """
        Return the reference of the general account 
        to be used to book the product movement of 
        the trade type and product.
        The default implementation works with the accounts created by
        :mod:`lino.modlib.accounts.fixtures.mini`.
        """
        if tt.name == 'sales':
            #~ return '7000'
            return 'sales'
        elif tt.name == 'purchases':
        #~ elif item.voucher.journal.type == JournalTypes.purchases:
            return 'purchases'
            #~ return '6000'
        
    #~ def get_sales_item_account(self,item):
        #~ return self.modules.accounts.Account.objects.get(group__ref='704000')
        
    def get_partner_account(self,voucher):
        """
        Return the reference of the general account 
        where the partner movement of the given voucher should be booked.
        The default implementation works with the accounts created by
        :mod:`lino.modlib.accounts.fixtures.mini`.
        """
        tt = voucher.get_trade_type()
        if tt.name == 'sales':
            #~ return '4000'
            return 'customers'
        elif tt.name == 'purchases':
            #~ return '4400'
            return 'suppliers'
        
    def get_vat_account(self,tt,vc,vr):
        """
        Return the reference of the account where the VAT amount should be booked.
        `tt` is a TradeType (usually either `sales` or `purchases`)
        `vc` is a VatClass
        `vr` is a VatRegime
        
        """
        if tt.name == 'sales':
            #~ return '4000'
            return 'vat_due'
        elif tt.name == 'purchases':
            #~ return '4400'
            return 'vat_deductible'
        
        #~ return '472100'

    def get_vat_rate(self,tt,vc,vr):
        VAT_RATES = dict(
          exempt=Decimal(),
          reduced=Decimal('0.07'),
          normal=Decimal('0.20')
        )
        return VAT_RATES[vc.name]

        
        
    def get_reminder_generators_by_user(self,user):
        """
        Override this per application to return a list of 
        reminder generators from all models for a give ueser
        A reminder generator is an object that has a `update_reminders` 
        method.
        """
        return []
        
    def install_migrations(self,*args):
        """
        See :func:`lino.utils.dumpy.install_migrations`.
        """
        from lino.utils.dumpy import install_migrations
        install_migrations(self,*args)
          
    #~ def get_application_info(self):
        #~ """
        
        #~ Application developers must implement 
        #~ this in their Lino 
        #~ subclass by something like this::
        
            #~ def get_application_info(self):
                #~ from myapp import __version__, __url__
                #~ return ("MyApp",__version__,__url__)
        
        #~ This function is used by 
        #~ :meth:`using` and :meth:`site_version`.
        
        #~ """
        #~ return (self.__name__,
                #~ self.__version__,
                #~ self.__url__)
        #~ return (self.django_settings['__name__'],
                #~ self.django_settings['__version__'],
                #~ self.django_settings['__url__'])
        #~ return ("Lino App",'0.1','http://code.google.com/p/lino/')
        
        #~ raise NotImplementedError()
        
    def using(self,ui=None):
        """
        Yields a list of (name, version, url) tuples
        describing the software used on this site.
        
        The first tuple describes the application itself.
        
        This function is used by 
        :meth:`welcome_text`,
        :meth:`welcome_html`
        and
        :meth:`site_version`.
        
        """
        from lino.utils import ispure
        assert ispure(self.short_name)
        
        #~ ai = self.get_application_info()
        #~ if ai is not None:
            #~ yield ai
        if self.short_name and self.version and self.url:
            yield (self.short_name, self.version, self.url)
        
        yield ("Lino",__version__,"http://lino.saffre-rumma.net")
        
        import django
        yield ("Django",django.get_version(),"http://www.djangoproject.com")
        
        import jinja2
        version = getattr(jinja2,'__version__','')
        yield ("Jinja",version,"http://jinja.pocoo.org/")
        
        import sphinx
        version = getattr(sphinx,'__version__','')
        yield ("Sphinx",version,"http://sphinx-doc.org/")
        
        import dateutil
        version = getattr(dateutil,'__version__','')
        yield ("python-dateutil",version,"http://labix.org/python-dateutil")
        
        try:
            import Cheetah
            version = Cheetah.Version 
        except ImportError:
            version = NOT_FOUND_MSG
        yield ("Cheetah",version ,"http://cheetahtemplate.org/")

        try:
            from odf import opendocument
            version = opendocument.__version__
        except ImportError:
            version = NOT_FOUND_MSG
        yield ("OdfPy",version ,"http://pypi.python.org/pypi/odfpy")

        try:
            import docutils
            version = docutils.__version__
        except ImportError:
            version = NOT_FOUND_MSG
        yield ("docutils",version ,"http://docutils.sourceforge.net/")

        try:
            import suds
            version = suds.__version__
        except ImportError:
            version = NOT_FOUND_MSG
        yield ("suds",version ,"https://fedorahosted.org/suds/")

        import yaml
        version = getattr(yaml,'__version__','')
        yield ("PyYaml",version,"http://pyyaml.org/")
        
        if False:
            try:
                import pyratemp
                version = getattr(pyratemp,'__version__','')
            except ImportError:
                version = NOT_FOUND_MSG
            yield ("pyratemp",version,"http://www.simple-is-better.org/template/pyratemp.html")
        
        if False:
            try:
                import ho.pisa as pisa
                version = getattr(pisa,'__version__','')
                yield ("xhtml2pdf",version,"http://www.xhtml2pdf.com")
            except ImportError:
                pass

            try:
                import reportlab
                version = reportlab.Version
            except ImportError:
                version = NOT_FOUND_MSG
            yield ("ReportLab",version,"http://www.reportlab.org/rl_toolkit.html")
                   
        try:
            #~ import appy
            from appy import version
            version = version.verbose
        except ImportError:
            version = NOT_FOUND_MSG
        yield ("Appy",version ,"http://appyframework.org/pod.html")
        
        import sys
        version = "%d.%d.%d" % sys.version_info[:3]
        yield ("Python",version,"http://www.python.org/")
        
        yield ("Silk Icons",'1.3',"http://www.famfamfam.com/lab/icons/silk/")

        if ui is not None:
            #~ version = '<script type="text/javascript">document.write(Ext.version);</script>'
            onclick = "alert('ExtJS client version is ' + Ext.version);"
            tip = "Click to see ExtJS client version"
            text = "(version)"
            #~ version = """<a href="#" onclick="%s" title="%s">%s</a>""" % (onclick,tip,text)
            version = xghtml.E.a(text,href='#',onclick=onclick,title=tip)
            yield ("ExtJS",version ,"http://www.sencha.com")
            
            if self.use_extensible:
                onclick = "alert('Extensible Calendar version is ' + Ext.ensible.version);"
                tip = "Click to see Extensible Calendar version"
                text = "(version)"
                #~ version = """<a href="#" onclick="%s" title="%s">%s</a>""" % (onclick,tip,text)
                version = xghtml.E.a(text,href='#',onclick=onclick,title=tip)
                yield ("Extensible",version ,"http://ext.ensible.com/products/calendar/")
            

    def welcome_text(self):
        """
        Text to display in a console window when Lino starts.
        """
        return "Using %s." % (', '.join(["%s %s" % (n,v) for n,v,u in self.using()]))

    def welcome_html(self,ui=None):
        """
        Text to display in the "about" dialog of a GUI application.
        """
        sep = '<br/>'
        #~ sep = ', '
        return sep.join(['<a href="%s" target="_blank">%s</a>&nbsp;%s' 
            % (u,n,v) for n,v,u in self.using(ui)])

    def site_version(self):
        """
        Used in footnote or header of certain printed documents.
        """
        name,version,url = self.using().next()
        #~ name,version,url = self.get_application_info()
        #~ if self.short_name
        #~ if self.version is None:
            #~ return self.short_name + ' (Lino %s)' % __version__
        #~ return self.short_name + ' ' + self.version
        return name + ' ' + version
        #~ return "Lino " + __version__


    #~ def watch_changes(self,model,fields=None,**options):
        #~ """
        #~ Declare a set of fields of a model to be "observed" or "watched".
        #~ Each change to an object comprising at least one watched 
        #~ will lead to an entry to the ChangesByObject table.
        
        #~ `model` may be a string `app.Model`.
        #~ It will be resolved during kernel startup.
        #~ All calls to watch_changes will be grouped by model.
        
        #~ See also :mod:`lino.utils.dblogger`.
        #~ """
        #~ self._watch_changes_requests.append((model,fields,options))
        
        
    #~ def setup_changelog(self):
    def on_site_startup(self):
        """
        This method is called during site startup
        """
        pass
        

    def get_system_note_recipients(self,ar,obj,silent):
        """
        Return or yield a list of recipients 
        (i.e. strings "Full Name <name@example.com>" )
        to be notified by email about a system note issued 
        by action request `ar` about the object instance `obj`.
        
        Default behaviour is to simply forwar it to the `obj`'s 
        :meth:`get_system_note_recipients <lino.core.model.Model.get_system_note_recipients>`,
        but here is a hook to define local exceptions to the 
        application specific default rules.
        """
        return obj.get_system_note_recipients(ar,silent)
        

    def get_todo_tables(self,ar):
        """
        Return or yield a list of tables that should be empty
        """
        for mod in self.get_installed_modules():
            meth = getattr(mod,'get_todo_tables',None)
            if meth is not None:
                #~ dblogger.debug("Running %s of %s", methname, mod.__name__)
                for i in meth(self,ar):
                    yield i

    
    def get_generic_related(self,obj):
        from django.contrib.contenttypes.models import ContentType
        for gfk in self.GFK_LIST:
            ct = ContentType.objects.get_for_model(gfk.model)
            kw = dict()
            kw[gfk.fk_field] = obj.pk
            yield gfk, ct.get_all_objects_for_this_type(**kw)
        
            