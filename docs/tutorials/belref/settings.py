from lino.projects.belref.settings import *


class Site(Site):
    default_ui = 'extjs'

SITE = Site(globals())

DEBUG = True

