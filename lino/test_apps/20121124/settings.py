from lino.apps.std.settings import *

class Lino(Lino):
  
    def get_installed_apps(self):
        yield 'lino.test_apps.20121124'
        
LINO = Lino(__file__,globals())    

