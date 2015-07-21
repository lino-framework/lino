# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.projects.std.settings import *


class Site(Site):

    verbose_name = "Lino Presto"
    version = "0.1"
    url = "http://lino-framework.org/examples/presto/"

    demo_fixtures = 'std few_languages props democfg demo demo2'.split()

    languages = 'en de fr et'

    project_model = 'tickets.Project'

    user_profiles_module = 'lino.projects.presto.roles'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contenttypes'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.properties'
        yield 'lino.projects.presto.lib.contacts'
        yield 'lino.modlib.households'
        yield 'lino.modlib.lists'
        yield 'lino.modlib.addresses'
        yield 'lino.modlib.humanlinks',
        yield 'lino.modlib.products'
        yield 'lino.modlib.accounts'
        # yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        yield 'lino.modlib.iban'
        yield 'lino.modlib.sepa'
        yield 'lino.modlib.finan'
        yield 'lino.modlib.auto.sales'
        #~ 'lino.modlib.projects',
        yield 'lino.modlib.blogs'
        yield 'lino.modlib.notes'
        # yield 'lino.modlib.tickets'
        yield 'lino.modlib.clocking'
        # yield 'lino.modlib.uploads'
        #~ 'lino.modlib.thirds',
        yield 'lino.modlib.extensible'
        yield 'lino.modlib.cal'
        # yield 'lino.modlib.outbox'
        # yield 'lino.modlib.excerpts'
        #~ yield 'lino.modlib.postings'
        #~ yield 'lino.modlib.pages'

        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.plausibility'
        yield 'lino.modlib.tinymce'

        yield 'lino.projects.presto.lib.presto'

    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.countries.configure(country_code='BE')

    def get_admin_main_items(self, ar):
        if False:
            from lino.utils.weekly import get_report

            def datefmt(d):
                T = self.modules.clocking.MySessionsByDate
                sar = T.request_from(
                    ar, param_values=dict(start_date=d, end_date=d))
                return ar.href_to_request(
                    sar, str(d.day), style="font-size:xx-small;")

            yield get_report(ar, datefmt=datefmt)
        yield self.modules.clocking.InvestedTimes
        # yield self.modules.tickets.MyTickets
        yield self.modules.tickets.ActiveTickets

