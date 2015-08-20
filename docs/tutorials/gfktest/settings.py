from lino.projects.std.settings import *


class Site(Site):

    catch_layout_exceptions = False

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.gfks'
        yield 'gfktest'

SITE = Site(globals())

DEBUG = True
