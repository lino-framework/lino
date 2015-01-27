from lino.projects.std.settings import *

# configure_plugin('countries', country_code='BE')


class Site(Site):

    verbose_name = "AddressLocation tutorial"

    demo_fixtures = ["few_countries", "few_cities", "demo"]

    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.countries.configure(country_code='BE')

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.countries'
        yield 'addrloc'


SITE = Site(globals())
