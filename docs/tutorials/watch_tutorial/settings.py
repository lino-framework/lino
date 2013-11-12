from lino import Site

class Site(Site):
    
    user_model = 'users.User'
    
    #~ demo_fixtures = "std few_countries few_cities demo demo2"
    demo_fixtures = "std demo demo2"
    
    languages = 'en'
    
    def get_installed_apps(self):
        
        for a in super(Site,self).get_installed_apps():
            yield a
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.changes'
        
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.notes'
        
        yield 'watch_tutorial'
        
        
    def setup_choicelists(self):
        """
        Redefines the default list of user profiles.
        """
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office')
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"),                  '_ _', 
            name='anonymous', readonly=True,authenticated=False)
        add('100', _("User"),                       'U U',name='user')
        add('900', _("Administrator"),              'A A',name='admin')
        

SITE = Site(globals())
SECRET_KEY = "20227" # see :djangoticket:`20227`
