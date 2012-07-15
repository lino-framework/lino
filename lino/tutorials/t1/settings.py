from lino.apps.std.settings import *

class Lino(Lino):
  
    title = "Lino Tutorial"
    
    #~ index_view_action = 'polls.Home'
    
    #~ anonymous_user_profile = '123'
    
    def setup_menu(self,ui,user,main):
        m = main.add_menu("polls","~Polls")
        m.add_action(self.modules.polls.Polls)
        m.add_action(self.modules.polls.Choices)
        
        super(Lino,self).setup_menu(ui,user,main)
        
        #~ m = main.add_menu("config","~Configure")
        #~ m.add_action(self.modules.users.Users)
        
LINO = Lino(__file__,globals()) 

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': abspath(join(dirname(__file__),'test.db'))
    }
}

INSTALLED_APPS = (
  'lino',
  #~ 'lino.modlib.users',
  'lino.tutorials.t1.polls'
)




