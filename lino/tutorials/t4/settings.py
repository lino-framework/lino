from lino.apps.min1.settings import *
class Lino(Lino):
    title = "Playing with minimal applications"
LINO = Lino(__file__,globals()) 

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'test.db',
    }
}

