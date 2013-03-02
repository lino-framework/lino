from lino import Site
SITE = Site(__file__,globals())
INSTALLED_APPS = [ 'lino.test_apps.quantityfield','lino','django_site']


#~ from lino.projects.std.settings import *
#~ class Lino(Lino):
    #~ user_model = None
#~ LINO = Lino(__file__,globals())    

#~ INSTALLED_APPS = (
  #~ 'lino.test_apps.quantityfield',
#~ )

