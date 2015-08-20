# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Default settings for :doc:`/igen/index`.

"""
import os
import sys
from os.path import join, dirname, normpath, abspath
from lino.projects.std.settings import *


class Site(Site):

    languages = ['en']

    title = "Lino/iGen"
    domain = "igen-demo.saffre-rumma.net"
    help_url = "http://lino.saffre-rumma.net/igen/index.html"

    #~ residence_permit_upload_type = None
    #~ work_permit_upload_type = None
    #~ driving_licence_upload_type = None
    # ledger_providers='4400',
    # ledger_customers='4000',
    # ~ sales_base_account = None # '7000',
    # ~ sales_vat_account = None # '4510',

    #~ def init_site_config(self,sc):
        #~ super(IgenSite,self).init_site_config(sc)
        #~ sc.next_partner_id = 200000

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.gfks'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'

        yield 'lino.modlib.contacts'
        #~ 'lino.modlib.notes'
        yield 'lino.modlib.extensible'
        yield 'lino.modlib.cal'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.products'
        #~ 'lino.modlib.journals',
        yield 'lino.modlib.vat'
        yield 'lino.modlib.accounts'
        yield 'lino.modlib.ledger'
        yield 'lino.modlib.sales'
        yield 'lino.modlib.finan'
        yield 'lino.modlib.uploads'
        yield 'lino.projects.igen'

    demo_fixtures = 'std few_languages few_countries few_cities demo_ee demo demo2'.split(
    )

SITE = Site(globals())
