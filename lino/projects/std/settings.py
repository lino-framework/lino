## Copyright 2009-2012 Luc Saffre
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

  from lino.projects.std.settings import *

"""

import os
import sys
import datetime
from tempfile import gettempdir
from os.path import join, abspath, dirname, normpath
import lino

from lino.ui import Lino

#~ class Lino(Lino):
    #~ pass
    

#~ 20130219 LINO = Lino(__file__,globals())

#~ DBLOGGER = 'db'
#~ DBLOGFILE = 'auto'
#~ USE_FIREBUG = False
#~ USE_GRIDFILTERS = True
#~ MODEL_DEBUG = True
#~ PROJECT_DIR = normpath(dirname(__file__))
#~ USER_INTERFACES = [
  #~ 'lino.ui.extjsu',
  #~ 'lino.ui.extjs'
  #~ ]
#~ DATA_DIR = join(LINO.project_dir,"data")

#~ BABEL_LANGS = []



def TIM2LINO_LOCAL(alias,obj):
    """Hook for local special treatment on instances that have been imported from TIM.
    """
    return obj
    
def TIM2LINO_USERNAME(userid):
    if userid == "WRITE": return None
    return userid.lower()
    
    
    

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG
#TEMPLATE_STRING_IF_INVALID = 'foo'


ADMINS = [
    # ('Your Name', 'your_email@domain.com'),
]

MANAGERS = ADMINS

if False:  
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
#~ TIME_ZONE = 'Europe/Brussels'
TIME_ZONE = None
# TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#~ LANGUAGE_CODE = 'de-BE'
#~ LANGUAGE_CODE = 'fr-BE'

#~ SITE_ID = 1 # see also fill.py

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

#~ MEDIA_ROOT = abspath(join(LINO.project_dir,'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#~ ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cqt^18t(Fb#14a@s%mbtdif+ih8fscpf8l9aw+0ivo2!3c(c%&'

#~ ROOT_URLCONF = 'lino.ui.extjs3.urls'

#~ TEMPLATE_DIRS = [
      #~ join(LINO.project_dir,'templates'),
      #~ join(abspath(dirname(lino.__file__)),'templates'),
#~ ]
#print "baz", __file__

#~ INSTALLED_APPS = [
  #~ 'lino.modlib.users',
  #~ 'lino',
#~ ]


#~ INSTALLED_APPS = []




#print "done", __file__

EMAIL_HOST = "mail.example.com"
#EMAIL_PORT = ""


#~ QOOXDOO_PATH = None
#~ """
#~ Path to the Qooxdoo SDK. Used by :term:`makeui`
#~ """

# this setting will be overridden by local settings
# it is needed for generating docs. Sphinx's autodoc needs to import the modules to introspect them, but Django would complain if no settings is specified.

#~ DATABASES = None

DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': ':memory:'
      }
  }


