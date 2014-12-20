# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""A special settings module to be used as DJANGO_SETTINGS_MODULE when
Sphinx generates the Lino docs.

It contains (almost) all modlib modules, which makes no sense in
practice and would maybe raise errors if you try to initialize a
database or validate the models, but it is enough to have autodocs do
its job.  And that's all we want.

"""

import os

from lino.projects.std.settings import *


class Site(Site):

    demo_fixtures = 'std few_countries euvatrates furniture \
    demo demo2'.split()

    verbose_name = "Lino Docs"

    project_model = 'contacts.Person'
    user_model = 'users.User'

    # languages = 'en de fr'
    languages = 'en de fr et nl pt-br es'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'lino.modlib.system'
        yield 'lino.modlib.contenttypes'
        yield 'lino.modlib.users'
        yield 'lino.modlib.changes'
        yield 'lino.modlib.languages'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.properties'
        yield 'lino.modlib.contacts'
        yield 'lino.modlib.addresses'
        yield 'lino.modlib.humanlinks'  # requires Person to be Born

        yield 'lino.modlib.uploads'
        yield 'lino.modlib.notes'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.extensible'
        yield 'lino.modlib.cal'
        # yield 'lino.modlib.reception'
        yield 'lino.modlib.excerpts'
        yield 'lino.modlib.polls'
        yield 'lino.modlib.cv'
        yield 'lino.modlib.postings'
        yield 'lino.modlib.households'

        yield 'lino.modlib.accounts'
        yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        yield 'lino.modlib.products'
        yield 'lino.modlib.auto.sales'
        yield 'lino.modlib.concepts'
        yield 'lino.modlib.courses'
        yield 'lino.modlib.pages'
        yield 'lino.modlib.iban'
        yield 'lino.modlib.sepa'
        yield 'lino.modlib.beid'
        #~ yield 'lino.projects.cosi'
        #~ yield 'lino'

    def setup_plugins(self):
        self.plugins.vat.configure(country_code='BE')
        super(Site, self).setup_plugins()

