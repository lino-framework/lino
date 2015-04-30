from lino.projects.presto.settings import *


class Site(Site):
    title = "mini tutorial"
    languages = 'en de fr'

SITE = Site(globals())

DEBUG = True

EMAIL_HOST = "your.smtp.host"
SERVER_EMAIL = 'you@example.com'

# uncomment the following line for testing in memory database:
#~ DATABASES['default']['NAME'] = ':memory:'
