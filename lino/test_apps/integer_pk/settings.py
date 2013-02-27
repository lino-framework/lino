from lino import Lino

#~ from lino.projects.std.settings import *

#~ class Lino(Lino):
  
    #~ def get_installed_apps(self):
        #~ yield 'lino.test_apps.integer_pk'
        
LINO = Lino(__file__,globals())    
INSTALLED_APPS = [ 'lino.test_apps.integer_pk','lino']
