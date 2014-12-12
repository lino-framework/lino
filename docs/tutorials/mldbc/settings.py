from lino.projects.std.settings import *

class Site(Site):

    title = "MLDBC Tutorial"

    languages = 'en fr'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        # yield 'lino.modlib.system'
        yield 'mldbc'

SITE = Site(globals())

DEBUG = True
