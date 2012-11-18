from lino.apps.std.settings import *

class Lino(Lino):
  
    title = "Cool Polls"
    
    #~ short_name = 'Lino Polls Tutorial'
    #~ version = '0.1'
    #~ url = 'http://lino-framework.org/tutorials/polls.html'
    
    def get_installed_apps(self):
        for a in super(Lino,self).get_installed_apps():
            yield a
        yield 'lino.apps.polls_tutorial.polls' # 'mysite.polls'

    def get_main_html(self,request):
        return self.modules.polls.Polls.recent_polls(request)
        
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
