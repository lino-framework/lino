from lino.projects.cosi.settings.demo import *
SITE = Site(globals(),title = "Lino-Cosi (:memory:)") 
DATABASES['default']['NAME'] = ':memory:'
