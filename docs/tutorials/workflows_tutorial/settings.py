## Copyright 2013 Luc Saffre
## This file is part of the Lino project.

from lino.projects.std.settings import *


class Site(Site):
    
    demo_fixtures = "std demo demo2"
    languages = 'en'
    
    def get_installed_apps(self):
        
        yield super(Site, self).get_installed_apps()
            
        yield 'lino.modlib.gfks'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.changes'
        
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        #~ yield 'lino_xl.lib.notes'
        
        yield 'workflows_tutorial'
        
    def setup_menu(self, profile, main):
        m = main.add_menu("entries", _("Entries"))
        m.add_action(MyEntries)
    
SITE = Site(globals())

