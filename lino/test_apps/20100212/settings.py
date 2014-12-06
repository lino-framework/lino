from lino.projects.std.settings import *


class Site(Site):
    user_model = None
SITE = Site(globals(), 'lino.test_apps.20100212')

# INSTALLED_APPS = (
#     'lino',
#     'lino.test_apps.20100212',  # Explaining Django ticket 12801
# )

#~ LOGGING = dict(filename='system.log',level='DEBUG',mode='w')
