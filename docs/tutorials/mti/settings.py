from lino.projects.std.settings import *


class Site(Site):

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'mti'

    def setup_menu(self, profile, main):
        m = main.add_menu("contacts", "Contacts")
        m.add_action('mti.Persons')
        m.add_action('mti.Places')
        m.add_action('mti.Restaurants')

SITE = Site(globals())
