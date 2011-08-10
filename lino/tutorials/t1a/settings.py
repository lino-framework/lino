from lino.apps.std.settings import *

class Lino(Lino):
  
    title = "Lino Tutorial"
    
LINO = Lino(__file__,globals()) 

from os.path import join, dirname, abspath

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': abspath(join(
            dirname(__file__),'..','..','..','tmp','t1.db')),
    }
}

INSTALLED_APPS = (
  'lino.modlib.users',
  'lino',
  'lino.tutorials.t1a.polls'
)




