from lino.apps.std.settings import *
class Lino(Lino):
    user_model = None
LINO = Lino(__file__,globals())    

INSTALLED_APPS = (
  #~ 'django.contrib.contenttypes', 
  'lino', 
  #~ 'lino.modlib.users', 
  #~ 'lino.modlib.contacts', 
  'lino.test_apps.1', # Lino and MTI
)

