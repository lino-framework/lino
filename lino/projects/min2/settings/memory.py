from .demo import *
SITE.verbose_name = SITE.verbose_name + " (:memory:)"
# SITE = Site(globals(), title=Site.title+" (:memory:)")
DATABASES['default']['NAME'] = ':memory:'
