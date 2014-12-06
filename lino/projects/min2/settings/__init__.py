# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)


from lino.projects.std.settings import *

class Site(Site):
    title = "Lino Mini 2"

    project_model = 'projects.Project'
    user_model = "users.User"

    #~ languages = ('de', 'fr')
    languages = 'en et'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.changes'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        # yield 'lino.modlib.uploads'
        # yield 'lino.modlib.outbox'
        yield 'lino.modlib.excerpts'
        yield 'lino.projects.min2.modlib.contacts'
        yield 'lino.modlib.addresses'
        yield 'lino.modlib.reception'
        yield 'lino.modlib.iban'
        yield 'lino.modlib.sepa'
        yield 'lino.modlib.notes'
        yield 'lino.modlib.projects'
        yield 'lino.modlib.humanlinks'
        yield 'lino.modlib.households'
        yield 'lino.modlib.cal'
        # yield 'lino.modlib.extensible'
        yield 'lino.modlib.pages'
        #~ yield 'lino.projects.min2'
        yield 'lino.modlib.export_excel'

    def setup_choicelists(self):
        """
        Defines a set of user profiles.
        """
        from django.utils.translation import ugettext_lazy as _
        from lino.modlib.users.mixins import UserProfiles
        UserProfiles.reset(
            '* office reception')
        add = UserProfiles.add_item
        add('000', _("Anonymous"),      '_ _ _',
            name='anonymous',
            readonly=True,
            authenticated=False)
        add('100', _("User"),           'U U U')
        add('900', _("Administrator"),  'A A A',
            name='admin')


