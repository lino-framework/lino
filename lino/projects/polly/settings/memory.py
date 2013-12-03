from lino.projects.polly.settings.demo import *
SITE = Site(globals(), title=Site.verbose_name + " (:memory:)")
DATABASES['default']['NAME'] = ':memory:'
