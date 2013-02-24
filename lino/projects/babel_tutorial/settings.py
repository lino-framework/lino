from lino.projects.std.settings import *
from lino_local import LocalLinoMixin 
class Lino(LocalLinoMixin,Lino):
  
    title = "Babel Tutorial"
    
    #~ languages = ['en']
    #~ languages = ['de', 'fr']
    languages = ['en', 'fr']
    
    def get_installed_apps(self):
        for a in super(Lino,self).get_installed_apps():
            yield a
        yield 'lino.projects.babel_tutorial' 

LINO = Lino(__file__,globals()) 

DEBUG = True

# The DATABASES setting is the only thing you should take 
# over from your original file:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': abspath(join(dirname(__file__),'test.db'))
    }
}
