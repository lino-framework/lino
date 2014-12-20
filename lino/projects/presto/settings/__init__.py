# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.projects.std.settings import *


class Site(Site):

    verbose_name = "Lino Presto"
    version = "0.1"
    url = "http://lino-framework.org/examples/presto/"

    demo_fixtures = 'std few_languages props democfg demo demo2'.split()

    languages = 'en de fr et'

    project_model = 'tickets.Project'
    user_model = 'users.User'

    # p = None
    # override_modlib_models = {
    #     'contacts.Person': p,
    #     'contacts.Company': p,
    #     'households.Household': p,
    #     'sales.Invoice': p,
    #     'sales.InvoiceItem': p}

    def setup_choicelists(self):
        """
        Defines application-specific default user profiles.
        Local site administrators can override this in their :xfile:.
        """
        from lino.modlib.users.mixins import UserProfiles
        from django.utils.translation import ugettext_lazy as _
        UserProfiles.reset('* office')
        add = UserProfiles.add_item
        add('000', _("Anonymous"),       '_ _', 'anonymous',
            readonly=True, authenticated=False)
        add('100', _("User"),            'U U', 'user')
        add('900', _("Administrator"),   'A A', 'admin')

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.properties'
        yield 'lino.projects.presto.modlib.contacts'
        yield 'lino.modlib.households'
        yield 'lino.modlib.lists'
        yield 'lino.modlib.addresses'
        yield 'lino.modlib.humanlinks',
        yield 'lino.modlib.products'
        yield 'lino.modlib.accounts'
        yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        yield 'lino.modlib.iban'
        yield 'lino.modlib.sepa'
        yield 'lino.modlib.finan'
        yield 'lino.modlib.auto.sales'
        #~ 'lino.modlib.projects',
        yield 'lino.modlib.blogs'
        yield 'lino.modlib.tickets'
        yield 'lino.modlib.uploads'
        #~ 'lino.modlib.thirds',
        yield 'lino.modlib.extensible'
        yield 'lino.modlib.cal'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.excerpts'
        #~ yield 'lino.modlib.postings'
        #~ yield 'lino.modlib.pages'

        yield 'lino.modlib.appypod'
        yield 'lino.modlib.export_excel'

        yield 'lino.projects.presto'

    def setup_plugins(self):
        self.plugins.vat.configure(country_code='BE')
        super(Site, self).setup_plugins()

