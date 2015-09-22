# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Default settings for a `lino.projects.min2` application.
"""

from lino.projects.std.settings import *


class Site(Site):
    """The parent of all :mod:`lino.projects.min2` applications.
    """
    title = "Lino Mini 2"
    project_model = 'projects.Project'
    languages = 'en et'
    user_profiles_module = 'lino.modlib.office.roles'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        # yield 'lino.modlib.users'
        yield 'lino.modlib.changes'
        yield 'lino.modlib.excerpts'
        yield 'lino.projects.min2.modlib.contacts'
        yield 'lino.modlib.addresses'
        yield 'lino.modlib.reception'
        # yield 'lino.modlib.sepa'
        yield 'lino.modlib.notes'
        yield 'lino.modlib.projects'
        yield 'lino.modlib.humanlinks'
        yield 'lino.modlib.households'
        yield 'lino.modlib.extensible'
        yield 'lino.modlib.pages'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.dupable_partners'
        yield 'lino.modlib.plausibility'
        yield 'lino.modlib.tinymce'

