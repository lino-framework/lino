from lino.apps.std.settings import *
INSTALLED_APPS = (
  'lino', 
  'lino.test_apps.20100212', # Explaining Django ticket 12801
)

LOGGING = dict(filename='system.log',level='DEBUG',mode='w')
