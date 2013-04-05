from lino.projects.std.settings import *

class Site(Site):
  
    title = "Cool Polls"
    languages = ['en'] # TODO: remove this here
    
    def get_installed_apps(self):
        for a in super(Site,self).get_installed_apps():
            yield a
        yield 'lino.projects.polls_tutorial.polls' # 'mysite.polls'

SITE = Site(globals()) 

DEBUG = True

# The DATABASES setting is the only thing you should take 
# over from your original file:
#~ DATABASES = {
    #~ 'default': {
        #~ 'ENGINE': 'django.db.backends.sqlite3', 
        #~ 'NAME': abspath(join(dirname(__file__),'test.db'))
    #~ }
#~ }
