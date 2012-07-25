from lino.apps.std.settings import *

class Lino(Lino):
  
    title = "Polls Tutorial"
    
    def setup_menu(self,ui,user,main):
        m = main.add_menu("polls","~Polls")
        m.add_action(self.modules.polls.Polls)
        m.add_action(self.modules.polls.Choices)
        super(Lino,self).setup_menu(ui,user,main)
        
    def get_main_html(self,request):
        from t1.polls import models as polls
        return polls.recent_polls(request)
        
LINO = Lino(__file__,globals()) 

DEBUG = True

INSTALLED_APPS = (
  'lino',
  't1.polls' # 'mysite.polls'
)

# The DATABASES setting is the only thing you should take 
# over from your original file:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': abspath(join(dirname(__file__),'test.db'))
    }
}
