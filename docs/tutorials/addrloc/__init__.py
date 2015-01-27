from lino.api import ad

class Plugin(ad.Plugin):
    verbose_name = "Addresses"

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('addrloc.Companies')
    
