# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
This is the base for all settings of lino.projects.min1

.. autosummary::
   :toctree:

   demo


"""

from lino.projects.std.settings import *


class Site(Site):
    title = "Lino Mini 1"

    languages = "en de"

    demo_fixtures = 'std demo demo2'

    def setup_quicklinks(self, ar, tb):
        tb.add_action(self.modules.contacts.Persons.detail_action)
        tb.add_action(self.modules.contacts.Companies.detail_action)

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.contacts'
        yield 'lino.modlib.cal'
        yield 'lino.modlib.export_excel'

    def get_admin_main_items(self, ar):
        yield self.modules.cal.MyEvents

    def setup_user_profiles(self):
        """
        Defines application-specific default user profiles.
        Local site administrators can override this in their :xfile:.
        """
        from lino.modlib.users.choicelists import (
            UserProfiles, Anonymous, SiteUser, StaffMember, SiteAdmin)
        from lino.modlib.office.choicelists import OfficeUser, OfficeStaff

        class SiteUser(OfficeUser): pass
        class StaffMember(StaffMember, OfficeStaff): pass
        class SiteAdmin(SiteAdmin, OfficeStaff): pass

        UserProfiles.clear()
        add = UserProfiles.add_item_instance
        add(Anonymous('000', name='anonymous',
                      readonly=True, authenticated=False))
        add(SiteUser('100',  name='user'))
        add(StaffMember('200', name='staff'))
        add(SiteAdmin('900', name='admin'))
