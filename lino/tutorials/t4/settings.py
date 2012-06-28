#~ from lino.apps.min1.settings import *
#~ from lino.apps.min2.settings import *
from lino.apps.presto.settings import *
class Lino(Lino):
    title = "Playing with minimal applications"
    #~ languages = ['en', 'de','fr']
    #~ languages = ['en']
    
LINO = Lino(__file__,globals()) 

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'test.db',
    }
}

