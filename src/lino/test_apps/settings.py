## Copyright 2008-2010 Luc Saffre
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

# Django settings file
# Works on Linux and Windows.

#print "begin", __file__

import os
import sys
from os.path import join,dirname, normpath, abspath
from tempfile import gettempdir

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG
#TEMPLATE_STRING_IF_INVALID = 'foo'

PROJECT_DIR = normpath(dirname(__file__))

ADMINS = (
    ('Luc Saffre', 'luc.saffre@gmx.net'),
    # ('Your Name', 'your_email@domain.com'),
)

# ADMINS is used in lino.utils.sites.LinoSite.password_reset()

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.

DATABASE_NAME = os.path.join(gettempdir(),'test_lino.db') 
DATABASE_NAME = ':memory:'

DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Tallinn'
# TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1 # see also fill.py

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# Used by FileSystemStorage
#MEDIA_ROOT = abspath(join(PROJECT_DIR,'..','media'))
MEDIA_ROOT = abspath(join(PROJECT_DIR,'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'



# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cqt^18t(Gb#14a@s%mbtdif+ih8fscpf8l9aw+0ivo2!3c(c%&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    #'lino.utils.editing.EditingMiddleware',
)

#ROOT_URLCONF = 'igen.demo.urls'
ROOT_URLCONF = 'urls'

import lino

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
      os.path.abspath(join(PROJECT_DIR,'templates')),
      os.path.abspath(join(dirname(lino.__file__),'templates')),
)
#print "baz", __file__

INSTALLED_APPS = (
  # 'lino.test_apps.example',
  'lino.test_apps.ledger',
  'lino.test_apps.20090714',
  'lino.test_apps.20090717', # Diamond inheritance (needs ticket #10808 to be fixed)
  'lino.test_apps.20091014', # assign floats to DecimalField
  'lino.test_apps.20100126', # Journals and Documents (needs ticket #10808 to be fixed)
)


SERIALIZATION_MODULES = {
     "data" : "lino.utils.dataserializer",
     "dpy" : "lino.utils.dpyserializer",
}

#print "done", __file__

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.auth",
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/"

#EMAIL_HOST = "mail.hot.ee"
#EMAIL_PORT = ""
#LINO_WEBMASTER = "luc.saffre@mail.ee"

#LINO_SETTINGS = os.path.join(PROJECT_DIR,"lino_settings.py")

#BYPASS_PERMS = True
BYPASS_PERMS = False

EXTJS_URL = "/extjs/"
if sys.platform == 'win32':
    EXTJS_ROOT = r's:\ext-3.1.0'
else:
   EXTJS_ROOT = None
   # don't serve extjs files because Apache does it
       
