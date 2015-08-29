# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)


import os
import lino

from lino.projects.std.settings import *


class Site(Site):
    #~ title = __name__
    version = "0.0.1"
    verbose_name = "Lino-HWS"
    url = "http://www.lino-framework.org/autodoc/lino.projects.homeworkschool"
    #~ author = "Luc Saffre"
    #~ author_email = "luc.saffre@gmx.net"

    #~ help_url = "http://lino.saffre-rumma.net/az/index.html"

    demo_fixtures = 'std few_languages demo demo2'.split(
    )

    #~ project_model = 'contacts.Person'
    #~ project_model = 'courses.Pupil'
    project_model = 'courses.Course'
    #~ project_model = None

    languages = ('en', 'de', 'fr')

    use_eid_jslib = False

    #~ index_view_action = "dsbe.Home"

    override_modlib_models = {
        'contacts.Person': None,
        'sales.Invoice': None,
        'sales.InvoiceItem': None,
    }

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.gfks'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        yield 'lino.modlib.households'
        yield 'lino.modlib.notes'
        yield 'lino.modlib.uploads'
        yield 'lino.modlib.extensible'
        yield 'lino.modlib.cal'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.pages'

        yield 'lino.modlib.accounts'
        yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        yield 'lino.modlib.products'
        yield 'lino.modlib.auto.sales'

        yield 'lino.modlib.courses'
        yield 'lino.projects.homeworkschool'

