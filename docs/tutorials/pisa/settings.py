from lino.projects.std.settings import *

class Site(Site):

    languages = 'en de fr'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'pisa'

SITE = Site(globals())

