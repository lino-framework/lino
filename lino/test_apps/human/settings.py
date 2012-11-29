from lino.apps.std.settings import *

class Lino(Lino):
    languages = ('en','de','fr')
    def get_installed_apps(self):
        for a in super(Lino,self).get_installed_apps(): yield a
        yield 'lino.test_apps.human'
        
LINO = Lino(__file__,globals())    

