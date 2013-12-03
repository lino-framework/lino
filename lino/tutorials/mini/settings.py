#~ from lino.projects.min1.settings import *
#~ from lino.projects.min2.settings import *
from lino.projects.presto.settings import *


class Site(Site):
    title = "mini tutorial"
    languages = ['en', 'de', 'fr']
    #~ languages = ['en']

SITE = Site(globals())

DEBUG = True

#~ DATABASES = {
    #~ 'default': {
        #~ 'ENGINE': 'django.db.backends.sqlite3',
        #~ 'NAME': 'test.db',
    #~ }
#~ }

LOGGING = dict(level='DEBUG')
#~ LOGGING = dict(filename=filename,level='DEBUG',rotate=False)
#~ LOGGING = dict(filename=join(SITE.project_dir,'log',filename),level='DEBUG')
#~ LOGGING = dict(filename=join(SITE.project_dir,'log',filename),level='DEBUG')
import datetime
filename = datetime.date.today().strftime('%Y-%m-%d.log')
logdir = join(SITE.project_dir, 'log')
import os
if os.path.exists(logdir):
    LOGGING.update(filename=join(logdir, filename))


EMAIL_HOST = "your.smtp.host"
SERVER_EMAIL = 'you@example.com'

# uncomment the following line for testing in memory database:
#~ DATABASES['default']['NAME'] = ':memory:'
