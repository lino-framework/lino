from lino.apps.std.settings import *

class Lino(Lino):
  
    title = "Lino Tutorial"
    
    def setup_menu(self,ui,user,main):
        m = main.add_menu("polls","~Polls")
        m.add_action(self.modules.polls.Polls)
        m.add_action(self.modules.polls.Choices)
        
        #~ m = main.add_menu("config","~Configure")
        #~ m.add_action(self.modules.users.Users)
        
LINO = Lino(__file__,globals()) 

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': abspath(join(
            dirname(__file__),'..','..','..','tmp','t1.db')),
    }
}

INSTALLED_APPS = (
  #~ 'django.contrib.contenttypes',
  #~ 'lino.modlib.users',
  'lino',
  'lino.tutorials.t1.polls'
)




