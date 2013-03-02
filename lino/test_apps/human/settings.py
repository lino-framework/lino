from lino.projects.std.settings import *

class Site(Site):
    languages = ('en','de','fr')
    def get_installed_apps(self):
        for a in super(Site,self).get_installed_apps(): yield a
        yield 'lino.test_apps.human'
        
SITE = Site(__file__,globals())    

