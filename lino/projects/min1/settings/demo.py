from lino.projects.min1.settings import *
from lino.utils import i2d


class Site(Site):
    the_demo_date = i2d(20141023)

SITE = Site(globals())
SECRET_KEY = "20227"  # see :djangoticket:`20227`
