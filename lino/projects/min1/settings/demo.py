from ..settings import *
from lino.utils import i2d
SITE = Site(globals(), the_demo_date=i2d(20141023))
SECRET_KEY = "20227"  # see :djangoticket:`20227`
