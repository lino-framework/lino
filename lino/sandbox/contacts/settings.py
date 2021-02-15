from lino.projects.std.settings import *


class Site(Site):
    user_model = 'contacts.User'
    #~ use_contenttypes = False

    abstract_address = True
    """
    If True, then the Addresses model is abstract 
    (i.e. we don't have a separate table for Addresses).
    After changing this setting, you must rebuild the database.
    """

    def setup_quicklinks(self, user, tb):
        super(Site, self).setup_quicklinks(user, tb)
        tb.add_action(self.modules.contacts.Persons.detail_action)
        tb.add_action(self.modules.contacts.Companies.detail_action)

    def setup_menu(self, user_type, main):
        from django.utils.translation import gettext_lazy as _
        from django.db import models

        def doit(methodname, *args):
            for a in models.get_apps():
                meth = getattr(a, methodname, None)
                if meth is not None:
                    meth(*args)

        m = main.add_menu("master", _("Master"))
        doit('setup_main_menu', self, ui, user_type, m)

        m = main.add_menu("config", _("Configure"))
        doit('setup_config_menu', self, ui, user_type, m)

        m = main.add_menu("explorer", _("Explorer"))
        doit('setup_explorer_menu', self, ui, user_type, m)

        m = main.add_menu("site", _("Site"))
        doit('setup_site_menu', self, ui, user_type, m)

SITE = Site(globals())

INSTALLED_APPS = (
    #~ 'django.contrib.contenttypes',
    'lino_xl.lib.countries',
    'lino',
    'lino.sandbox.contacts',
)

import datetime
filename = settings.SITE.today().strftime('%Y-%m-%d.log')
LOGGING = dict(filename=join(LINO.project_dir, 'log', filename), level='DEBUG')


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(LINO.project_dir, 'test.db')
        #~ 'NAME': ':memory:'
    }
}
# uncomment for testing in temporary database:
#~ DATABASES['default']['NAME'] = ':memory:'
