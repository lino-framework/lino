from .demo import *
SITE = Site(globals(), title="min1 (:memory:)")
DATABASES['default']['NAME'] = ':memory:'
