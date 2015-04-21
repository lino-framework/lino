from lino.projects.std.settings import *


class Site(Site):

    title = "Lino LETS Tutorial"

    def setup_menu(self, profile, main):
        m = main.add_menu("master", "Master")
        m.add_action(self.modules.lets.Members)
        m.add_action(self.modules.lets.Products)

        m = main.add_menu("market", "Market")
        m.add_action(self.modules.lets.Offers)
        m.add_action(self.modules.lets.Demands)

        m = main.add_menu("config", "Configure")
        m.add_action(self.modules.lets.Places)

    def get_admin_main_items(self, ar):

        yield self.modules.lets.ActiveProducts

SITE = Site(globals(), 'lets')

DEBUG = True

