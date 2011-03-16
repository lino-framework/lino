## Copyright 2009-2011 Luc Saffre
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

"""
This defines Lino default settings. You include this (directly or indirectly) 
into your local :xfile:`settings.py` using::

  from lino.demos.std.settings import *

"""

import os
import sys
from tempfile import gettempdir
from os.path import join, abspath, dirname, normpath
import lino


class Lino(object):
    """
    Base class for the Lino Application instance stored in :setting:`LINO`.
    
    Lino classes are defined and instantiated in Django settings files.
    
    This class is first defined in :mod:`lino.demos.std.settings`,
    then subclassed by :mod:`lino.apps.myapp.settings`
    which is probably subclassed by your local :xfile:`settings.py`
    
    """
    help_url = "http://code.google.com/p/lino"
    #~ index_html = "This is the main page."
    title = "Base Lino Application"
    domain = "www.example.com"
    
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
    
    source_dir = os.path.dirname(__file__)
    
    def __init__(self,project_file):
        #self.django_settings = settings
        #~ self.init_site_config = lambda sc: sc
        self.project_dir = normpath(dirname(project_file))
        self.dummy_messages = set()
        self._setting_up = False
        self._setup_done = False
        self.root_path = '/lino/'
        self._response = None
        self.source_name = os.path.split(self.source_dir)[-1]
        #~ # find the first base class that is defined in the Lino source tree
        #~ # this is to find out the source_name and the source_dir
        #~ for cl in self.__class__.__mro__:
            #~ if cl.__module__.startswith('lino.apps.'):
                #~ self.source_dir = os.path.dirname(__file__)
                #~ self.source_name = self.source_dir
                #~ os.path.split(_source_dir,
              
            
        # ImportError: Settings cannot be imported, because environment variable DJANGO_SETTINGS_MODULE is undefined.
        #~ from lino.models import get_site_config
        #~ self.config = get_site_config()
        

    def add_dummy_message(self,s):
        self.dummy_messages.add(s)
            
        
        
    def setup_main_menu(self):
        pass
          
    def init_site_config(self,sc):
        #~ self.config = sc
        pass
        
    def configure(self,sc):
        self.config = sc
        
    def setup(self):
      
        from lino.core.kernel import setup_site
        #~ from lino.site import setup_site

        setup_site(self)

        
    def add_menu(self,*args,**kw):
        return self.main_menu.add_menu(*args,**kw)

    def context(self,request,**kw):
        d = dict(
          main_menu = menus.MenuRenderer(self.main_menu,request),
          root_path = self.root_path,
          lino = self,
          settings = settings,
          debug = True,
          #skin = self.skin,
          request = request
        )
        d.update(kw)
        return d
        
    def select_ui_view(self,request):
        html = '<html><body>'
        html += 'Please select a user interface: <ul>'
        for ui in self.uis:
            html += '<li><a href="%s">%s</a></li>' % (ui.name,ui.verbose_name)
        html += '</ul></body></html>'
        return HttpResponse(html)
        
        
    #~ def get_urls(self):
        #~ assert self._setup_done
        #~ if len(self.uis) == 1:
            #~ return self.uis[0].get_urls()
        #~ urlpatterns = patterns('',
            #~ ('^$', self.select_ui_view))
        #~ for ui in self.uis:
            #~ urlpatterns += patterns('',
                #~ (ui.name, include(ui.get_urls())),
            #~ )
        #~ return urlpatterns
        
    def get_site_menu(self,user):
        #~ self.setup()
        assert self._setup_done
        return self.main_menu.menu_request(user)
        
    #~ def add_program_menu(self):
        #~ return
        #~ m = self.add_menu("app","~Application",)
        #~ m.add_item(url="/accounts/login/",label="Login",can_view=perms.is_anonymous)
        #~ m.add_item(url="/accounts/logout/",label="Logout",can_view=perms.is_authenticated)
        #m.add_item(system.Login(),can_view=perms.is_anonymous)
        #m.add_item(system.Logout(),can_view=perms.is_authenticated)
        
    def setup_dblogger(self,logger):
        """
        Called when settings.DBLOGFILE is not empty *and* a logger 'db' 
        hasn't been configured manually.
        See :mod:`lino.utils.dblogger`
        """
        logger.setLevel(logging.INFO)
      


LINO = Lino(__file__)

#~ DBLOGGER = 'db'
DBLOGFILE = 'auto'
USE_FIREBUG = False
USE_GRIDFILTERS = True
MODEL_DEBUG = True
#~ PROJECT_DIR = normpath(dirname(__file__))
BYPASS_PERMS = False
USER_INTERFACES = [
  #~ 'lino.ui.extjsu',
  'lino.ui.extjs'
  ]
#~ DATA_DIR = join(LINO.project_dir,"data")

#~ BABEL_LANGS = []

APPY_PARAMS = dict(ooPort=8100)
try:
    import uno
except ImportError:
    APPY_PARAMS.update(pythonWithUnoPath=r'C:\PROGRA~1\LIBREO~1\program\python.exe')
    #~ APPY_PARAMS.update(pythonWithUnoPath=r'C:\PROGRA~1\OPENOF~1.ORG\program\python.exe')
    #~ APPY_PARAMS.update(pythonWithUnoPath='/usr/bin/libreoffice')
    #~ APPY_PARAMS.update(pythonWithUnoPath='/etc/openoffice.org3/program/python')


def TIM2LINO_LOCAL(alias,obj):
    """Hook for local special treatment on instances that have been imported from TIM.
    """
    return obj
    
def TIM2LINO_USERNAME(userid):
    if userid == "WRITE": return None
    return userid.lower()
    
    
def TIM2LINO_IS_IMPORTED_PARTNER(obj):
    "`obj` is either a Person or a Company"
    #~ return obj.id is not None and (obj.id < 200000 or obj.id > 299999)
    return False
    #~ return obj.id is not None and (obj.id > 10 and obj.id < 21)
              
    

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG
#TEMPLATE_STRING_IF_INVALID = 'foo'


ADMINS = (
    ('Luc Saffre', 'luc.saffre@gmx.net'),
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(LINO.project_dir,'demo.db')
        #~ 'NAME': ':memory:'
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Brussels'
# TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#~ LANGUAGE_CODE = 'de-BE'
#~ LANGUAGE_CODE = 'fr-BE'

SITE_ID = 1 # see also fill.py

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# Used by FileSystemStorage.
# Lino generates the :xfile:`site.js` there.
#~ if sys.platform == 'win32': # development server
    #~ MEDIA_ROOT = abspath(join(PROJECT_DIR,'media'))
#~ else:
    #~ MEDIA_ROOT = abspath(join(DATA_DIR,'media'))

MEDIA_ROOT = abspath(join(LINO.project_dir,'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cqt^18t(Fb#14a@s%mbtdif+ih8fscpf8l9aw+0ivo2!3c(c%&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

"""
Django and standard HTTP authentication.
http://stackoverflow.com/questions/152248/can-i-use-http-basic-authentication-with-django
"""

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    #~ 'django.contrib.sessions.middleware.SessionMiddleware',
    #~ 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'lino.modlib.auth.middleware.RemoteUserMiddleware',
    'django.middleware.doc.XViewMiddleware',
    #'lino.utils.editing.EditingMiddleware',
]


if False: # not BYPASS_PERMS:
    MIDDLEWARE_CLASSES += (
      'django.contrib.auth.middleware.RemoteUserMiddleware',
    )
    AUTHENTICATION_BACKENDS = (
      'django.contrib.auth.backends.RemoteUserBackend',
    )
    
if False:
    MIDDLEWARE_CLASSES += (
      #~ 'lino.utils.sqllog.ShortSQLLogToConsoleMiddleware',
      'lino.utils.sqllog.SQLLogMiddleware',
    )
    

ROOT_URLCONF = 'lino.ui.extjs.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
      #~ join(abspath(DATA_DIR),'templates'),
      join(abspath(LINO.project_dir),'templates'),
      join(abspath(dirname(lino.__file__)),'templates'),
)
#print "baz", __file__

INSTALLED_APPS = [
  #~ 'django.contrib.auth',
  'lino.modlib.auth',
  'django.contrib.contenttypes',
  #~ 'django.contrib.sessions',
  'django.contrib.sites',
  #~ 'django.contrib.markup',
  #~ 'django.contrib.databrowse',
  
  'lino',
  #~ 'lino.modlib.countries',
  #~ 'lino.modlib.contacts',
  #~ 'lino.modlib.products',
  #~ 'lino.modlib.projects',
  #~ 'lino.modlib.notes',
  
  #~ 'lino.modlib.journals',
  #~ 'lino.modlib.sales',
  #~ 'lino.modlib.ledger',
  #~ 'lino.modlib.finan',
  
  #~ 'lino.modlib.properties',
  #~ 'lino.modlib.links',
  #~ 'lino.modlib.dsbe',
  #~ 'lino.modlib.igen',
  #~ 'south', # http://south.aeracode.org
]


#~ INSTALLED_APPS = []



SERIALIZATION_MODULES = {
     #~ "data" : "lino.utils.dataserializer",
     "dpy" : "lino.utils.dpy",
}

#print "done", __file__

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.auth",
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/"

EMAIL_HOST = "mail.example.com"
#EMAIL_PORT = ""

LOGGING_CONFIG = 'lino.utils.log.configure'
LOGGING = dict(filename=None,level='INFO')


gettext = lambda s: s

def language_choices(*args):
    """
    See :doc:`/blog/2011/0226`.
    A subset of Django's LANGUAGES.
    """
    _langs = dict(
        en=gettext('English'),
        de=gettext('German'),
        fr=gettext('French'),
        nl=gettext('Dutch'),
        et=gettext('Estonian'),
    )
    return [(x,_langs[x]) for x in args]
      
LANGUAGES = language_choices('en','de','fr','nl','et')

QOOXDOO_PATH = None
"""
Path to the Qooxdoo SDK. Used by :term:`makeui`
"""



