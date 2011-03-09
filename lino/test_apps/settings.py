## Copyright 2008-2011 Luc Saffre
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

from lino.apps.std.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG
#TEMPLATE_STRING_IF_INVALID = 'foo'

PROJECT_DIR = normpath(dirname(__file__))
if sys.platform == 'win32':
    DATA_DIR = 'C:\\Temp\\test_apps\\'
else:
    #~ EXTJS_ROOT = None # don't serve extjs files because Apache does it
    DATA_DIR = '/usr/local/lino/test_apps/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #~ 'NAME': join(DATA_DIR,'test_apps.db')
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = (

  'lino', 
  # modlib apps required by some test_apps
  #~ 'lino.modlib.contacts', 
  #~ 'lino.modlib.journals', 
  #~ 'lino.modlib.properties',
  #~ 'django.contrib.contenttypes',
  
  # apps that test and document Lino features
  #~ 'lino.test_apps.journals',  
  #~ 'lino.test_apps.properties',
  #~ 'lino.test_apps.chooser', 
  
  # apps that test some specific problem encountered
  #~ 'lino.test_apps.20090714',
  #~ 'lino.test_apps.20090717', # Diamond inheritance (needs ticket #10808 to be fixed)
  #~ 'lino.test_apps.20091014', # assign floats to DecimalField
  'lino.test_apps.20100126', # Journals and Documents (needs ticket #10808 to be fixed)
  #~ 'lino.test_apps.20100127', # Django raises DoesNotExist when consulting an empty ForeignKey field
  #~ 'lino.test_apps.20100206', # 
  
  #~ 'lino.test_apps.20100212', # Explaining Django ticket 12801
  #~ 'lino.test_apps.20100519', # Cannot define primary_key field in abstact Model
  'lino.test_apps.1', # Lino and MTI
  #~ 'lino.test_apps.2', # Turn a Restaurant into a simple Place
)

LOGGING = dict(filename='system.log',level='DEBUG',mode='w')
