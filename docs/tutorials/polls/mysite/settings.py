from lino.projects.std.settings import *

#~ class Site(Site):
  
    #~ title = "Cool Polls"
    
    #~ def get_installed_apps(self):
        #~ for a in super(Site,self).get_installed_apps():
            #~ yield a
        #~ yield 'mysite.polls' 

#~ SITE = Site(__file__,globals()) 

SITE = Site(__file__,globals(),'polls',title="Cool Polls")

DEBUG = True

