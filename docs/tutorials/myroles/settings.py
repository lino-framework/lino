from lino.projects.polly.settings import *


class Site(Site):

    user_profiles_module = 'myroles.myroles'

SITE = Site(globals())

# SECRET_KEY = 123
# DEBUG = True
