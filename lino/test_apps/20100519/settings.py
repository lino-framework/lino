from lino.projects.std.settings import *

class Lino(Lino):
  
    def get_installed_apps(self):
        yield 'lino.test_apps.20100519'
        
LINO = Lino(__file__,globals())    

