from .demo import *
SITE.verbose_name = SITE.verbose_name + " (:memory:)"
# SITE = Site(globals(), title="min1 (:memory:)")
DATABASES['default']['NAME'] = ':memory:'
