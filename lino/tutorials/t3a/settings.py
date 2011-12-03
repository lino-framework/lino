from lino.apps.std.settings import *

class Lino(Lino):
  
    title = "Lino LETS Tutorial (1)"
    
    user_model = None
    
    def setup_menu(self,ui,user,main):
        m = main.add_menu("master","Master")
        m.add_action('lets.Products')
        m.add_action('lets.Customers')
        m.add_action('lets.Providers')
        
        m = main.add_menu("master","Market")
        m.add_action('lets.Offers')
        m.add_action('lets.Demands')
        
        m = main.add_menu("config","Configure")
        #~ m.add_action('users.Users')
        m.add_action('lets.Places')
    
    
LINO = Lino(__file__,globals()) 

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': abspath(join(
            dirname(__file__),'..','..','..','tmp','t3.db')),
    }
}

INSTALLED_APPS = (
  'django.contrib.contenttypes',
  #~ 'lino.modlib.users',
  'lino',
  'lino.tutorials.t3a.lets'
)

