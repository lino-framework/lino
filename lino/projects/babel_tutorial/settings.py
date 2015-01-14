from lino.projects.std.settings import *
#~ from lino_local import LocalLinoMixin


class Site(Site):

    title = "Babel Tutorial"

    #~ languages = ['en']
    #~ languages = ['de', 'fr']
    languages = ['en', 'fr']

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.system'
        yield 'lino.projects.babel_tutorial'

    def setup_menu(self, profile, main):
        m = main.add_menu("products", "Products")
        m.add_action(self.modules.babel_tutorial.Products)
    
SITE = Site(globals())

DEBUG = True

# The DATABASES setting is the only thing you should take
# over from your original file:
#~ DATABASES = {
    #~ 'default': {
        #~ 'ENGINE': 'django.db.backends.sqlite3',
        #~ 'NAME': abspath(join(dirname(__file__),'test.db'))
    #~ }
#~ }
