from lino.projects.std.settings import *

class Site(Site):

    languages = 'en de de-be'

    def setup_menu(self, profile, main):
        m = main.add_menu("master", "Master")
        m.add_action('de_BE.Expressions')
    
    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'de_BE'


SITE = Site(globals())
