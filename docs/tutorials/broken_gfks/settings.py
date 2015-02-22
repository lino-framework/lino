from lino.projects.std.settings import *

class Site(Site):

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'lino.modlib.contenttypes'

SITE = Site(globals(), 'broken_gfks')

DEBUG = True
