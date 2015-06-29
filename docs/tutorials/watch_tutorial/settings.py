## This file is part of the Lino project.

from lino.projects.std.settings import *


class Site(Site):

    demo_fixtures = "std demo demo2"
    languages = 'en'
    default_user = "robin"
    disable_user_roles = True

    def get_installed_apps(self):

        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.notes'
        yield 'lino.modlib.changes'

        yield 'watch_tutorial'


SITE = Site(globals(), no_local=True)

DEBUG = True
