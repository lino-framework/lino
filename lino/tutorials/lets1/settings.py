from lino.projects.std.settings import *


class Site(Site):

    title = "Lino LETS Tutorial (1)"

    #~ user_model = None

    def setup_menu(self, ui, profile, main):
        m = main.add_menu("master", "Master")
        m.add_action(self.modules.lets.Products)
        m.add_action(self.modules.lets.Customers)
        m.add_action(self.modules.lets.Providers)

        m = main.add_menu("market", "Market")
        m.add_action(self.modules.lets.Offers)
        m.add_action(self.modules.lets.Demands)

        m = main.add_menu("config", "Configure")
        #~ m.add_action('users.Users')
        m.add_action(self.modules.lets.Places)


#~ SITE = Site(globals(),'lino.modlib.users','lino.tutorials.lets1.lets')
SITE = Site(globals(), 'lino.tutorials.lets1.lets')

DEBUG = True

