## Copyright 2009-2010 Luc Saffre
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

import lino

from lino.demos.std.settings import *

PROJECT_DIR = abspath(dirname(__file__))
DATA_DIR = join(PROJECT_DIR,"data")
#~ LINO_SETTINGS = join(PROJECT_DIR,"lino_settings.py")
from lino.demos.dsbe.site import Site
LINO_SITE = Site()

MEDIA_ROOT = join(PROJECT_DIR,'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(DATA_DIR,'dsbe_demo.db')
        #~ 'NAME': ':memory:'
    }
}


TIME_ZONE = 'Europe/Brussels'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-BE'
#~ LANGUAGE_CODE = 'fr-BE'

#~ ROOT_URLCONF = 'lino.demos.dsbe.urls'

SITE_ID = 1 # see also fill.py

INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  #~ 'django.contrib.markup',
  #~ 'lino.modlib.system',
  'lino',
  'lino.modlib.countries',
  #~ 'lino.modlib.documents',
  #~ 'lino.modlib.properties',
  'lino.modlib.contacts',
  #~ 'lino.modlib.projects',
  'lino.modlib.notes',
  'lino.modlib.links',
  'lino.modlib.uploads',
  #'dsbe.modlib.contacts',
  #'dsbe.modlib.projects',
  'lino.modlib.dsbe',
  'south', # http://south.aeracode.org
)

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (
      join(abspath(DATA_DIR),'templates'),
      join(abspath(PROJECT_DIR),'templates'),
      join(abspath(dirname(lino.__file__)),'templates'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cqt^18t(Fb#14a@s%mbtdif+ih8fscpf8l9aw+0ivo2!3c(c%&'


#~ __all__ = [x for x in dir() if x[0].isupper()]

