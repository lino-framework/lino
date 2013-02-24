from lino.projects.std.settings import *
LINO = Lino(__file__,globals())    

INSTALLED_APPS = (
  'lino', 
  'lino.test_apps.nomti', 
)

