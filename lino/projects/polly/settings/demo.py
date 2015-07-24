from lino.projects.polly.settings import *
from lino.utils import i2d


class Site(Site):
    title = Site.verbose_name + " demo"
    the_demo_date = i2d(20141023)

SITE = Site(globals())

#~ DEBUG=True
# the following line should always be commented out in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
