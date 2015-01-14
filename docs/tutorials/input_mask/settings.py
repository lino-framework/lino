from lino.projects.std.settings import *


class Site(Site):

    def get_installed_apps(self):
        
        yield super(Site, self).get_installed_apps()
        yield 'input_mask'

    def setup_menu(self, profile, main):
        m = main.add_menu("foos", "Input Mask")
        m.add_action('input_mask.Foos')

SITE = Site(globals())
