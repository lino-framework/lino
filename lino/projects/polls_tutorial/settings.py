from lino.projects.std.settings import *

class Lino(Lino):
  
    title = "Cool Polls"
    
    def get_installed_apps(self):
        for a in super(Lino,self).get_installed_apps():
            yield a
        yield 'lino.projects.polls_tutorial.polls' # 'mysite.polls'

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
