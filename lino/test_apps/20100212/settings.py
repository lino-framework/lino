from lino.apps.std.settings import *
class Lino(Lino):
    user_model = None
LINO = Lino(__file__,globals())    

INSTALLED_APPS = (
  'lino', 
  'lino.test_apps.20100212', # Explaining Django ticket 12801
)

#~ LOGGING = dict(filename='system.log',level='DEBUG',mode='w')
