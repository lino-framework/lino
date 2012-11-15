from lino.apps.std.settings import *

__name__ = 'Lino Polls Tutorial'
__version__ = '0.1'
__url__ = 'http://lino-framework.org/tutorials/polls.html'

class Lino(Lino):
  
    title = "Cool Polls"
    
    def get_application_info(self):
        return (__name__,__version__,__url__)
    
    def setup_menu(self,ui,user,main):
        m = main.add_menu("polls","~Polls")
        m.add_action(self.modules.polls.Polls)
        m.add_action(self.modules.polls.Choices)
        super(Lino,self).setup_menu(ui,user,main)
        
    def get_installed_apps(self):
        for a in super(Lino,self).get_installed_apps():
            yield a
        yield 'lino.tutorials.t1.polls' # 'mysite.polls'

    def get_main_html(self,request):
        from lino.tutorials.t1.polls.models import recent_polls
        return recent_polls(request)
        
LINO = Lino(__file__,globals()) 

DEBUG = True

#~ INSTALLED_APPS = (
  #~ 'lino',
  #~ 't1.polls' # 'mysite.polls'
#~ )

# The DATABASES setting is the only thing you should take 
# over from your original file:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': abspath(join(dirname(__file__),'test.db'))
    }
}
