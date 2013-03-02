from lino.projects.std.settings import *
Site = Site(__file__,globals())    

INSTALLED_APPS = (
  'lino', 
  'lino.test_apps.nomti', 
)

