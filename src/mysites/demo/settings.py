## Copyright 2008-2009 Luc Saffre.
## This file is part of the Lino project. 

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

# Django settings file
# Works on Linux and Windows.

#print "begin", __file__

import os
import sys
from tempfile import gettempdir

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG
#TEMPLATE_STRING_IF_INVALID = 'foo'

PROJECT_DIR = os.path.normpath(os.path.dirname(__file__))

ADMINS = (
    ('Luc Saffre', 'luc.saffre@gmx.net'),
    # ('Your Name', 'your_email@domain.com'),
)

# ADMINS is used in lino.django.utils.sites.LinoSite.password_reset()

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.

DATABASE_NAME = os.path.join(gettempdir(),'mysites_demo.db') 
#DATABASE_NAME = ':memory:'
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

SITE_ID = 1 # see also reset_demo.py

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# Used by FileSystemStorage
MEDIA_ROOT = os.path.abspath(os.path.join(
  PROJECT_DIR, '..', 'media'))

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
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'lino.django.utils.editing.EditingMiddleware',
)

ROOT_URLCONF = 'mysites.demo.urls'

#print "foo", __file__

#~ try:
#~ except Exception,e:
    #~ import traceback
    #~ traceback.print_exc(e)
    #~ raise e


#print "bar", __file__

from lino.django import templates

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
      os.path.abspath(os.path.join(PROJECT_DIR,'templates')),
      os.path.abspath(os.path.dirname(templates.__file__)),
)
#print "baz", __file__

if True:
  INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.admin',
    'django.contrib.databrowse',
    
    'lino.django.apps.system',
    'lino.django.apps.countries',
    'lino.django.apps.contacts',
    'lino.django.apps.products',
    'lino.django.apps.documents',
    'lino.django.apps.ledger',
    'lino.django.apps.sales',
    'lino.django.apps.finan',
    'lino.django.apps.journals',
    
    #'lino.django.apps.voc',
    #'lino.django.apps.songs',
  )
else:
  INSTALLED_APPS = (
    #'lino.django.test_apps.contacts',
    #'lino.django.test_apps.sales',
    #'lino.django.test_apps.example',
    #'lino.django.test_apps.ledger',
    #'lino.django.test_apps.20090714',
    'lino.django.test_apps.20090717',
  )


SERIALIZATION_MODULES = {
     "data" : "lino.django.utils.dataserializer",
     "dpy" : "lino.django.utils.dpyserializer",
}

#print "done", __file__

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.auth",
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/"

EMAIL_HOST = "mail.hot.ee"
#EMAIL_PORT = ""
#LINO_WEBMASTER = "luc.saffre@mail.ee"

LINO_SETTINGS = os.path.join(PROJECT_DIR,"lino_settings.py")

EXTJS_URL = "/extjs/"
if sys.platform == 'win32':
    EXTJS_ROOT = r's:\ext-3.0.0'
    #~ if os.path.exists(extjs_root):
        #~ from django.core.files.storage import FileSystemStorage
        #~ fs = FileSystemStorage(location=extjs_root,base_url=EXTJS_URL)
        #~ print extjs_root
else:
   EXTJS_ROOT = None
        
#print "ok"