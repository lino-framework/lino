from .demo import *
SITE = Site(globals(), title="Lino-Cosi (:memory:)", no_local=True)
DATABASES['default']['NAME'] = ':memory:'
