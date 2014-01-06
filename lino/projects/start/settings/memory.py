from .demo import *
SITE = Site(globals(), title=Site.title+" (:memory:)")
DATABASES['default']['NAME'] = ':memory:'
