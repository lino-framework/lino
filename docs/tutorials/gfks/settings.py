from lino.projects.std.settings import *


class Site(Site):

    catch_layout_exceptions = False

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contenttypes'
        yield 'gfks'

SITE = Site(globals())

DEBUG = True
