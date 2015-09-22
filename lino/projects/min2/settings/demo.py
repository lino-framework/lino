from lino.api import ad
from lino.projects.min2.settings import *
from lino.utils import i2d

ad.configure_plugin('sepa', import_statements_path="/home/khchine5/Documents/Documentation/Lino/Ticket 505/test_file")

SITE = Site(globals(), the_demo_date=i2d(20141023))
ALLOWED_HOSTS = ['*']
DEBUG = True
SECRET_KEY = "20227"  # see :djangoticket:`20227`
