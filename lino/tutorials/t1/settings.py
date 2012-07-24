from lino.apps.std.settings import *

class Lino(Lino):
  
    title = "Polls Tutorial"
    
    def setup_menu(self,ui,user,main):
        m = main.add_menu("polls","~Polls")
        m.add_action(self.modules.polls.Polls)
        m.add_action(self.modules.polls.Choices)
        super(Lino,self).setup_menu(ui,user,main)
        
    def get_main_action(self,user):
        #~ return self.modules.polls.PollsList.default_action
        return None
    
    def get_main_html(self,request):
        from lino.tutorials.t1.polls import models as polls
        return polls.recent_polls(request)
        
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
  'lino.tutorials.t1.polls'
)




