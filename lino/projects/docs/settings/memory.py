from .demo import *
SITE = Site(globals(), title="(:memory:)")
DATABASES['default']['NAME'] = ':memory:'
