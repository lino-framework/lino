from lino.projects.std.settings import *


class Site(Site):

    verbose_name = "Lino LETS MTI Tutorial"

    def setup_menu(self, profile, main):
        m = main.add_menu("master", "Master")
        m.add_action(self.modules.letsmti.Members)
        m.add_action(self.modules.letsmti.Customers)
        m.add_action(self.modules.letsmti.Suppliers)
        m.add_action(self.modules.letsmti.Products)

        m = main.add_menu("market", "Market")
        m.add_action(self.modules.letsmti.Offers)
        m.add_action(self.modules.letsmti.Demands)

        m = main.add_menu("config", "Configure")
        m.add_action(self.modules.letsmti.Places)

    def get_admin_main_items(self, ar):

        yield self.modules.letsmti.ActiveProducts

SITE = Site(globals(), 'letsmti')

DEBUG = True

