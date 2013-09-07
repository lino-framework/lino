from lino import Site
SITE = Site(globals(),
    'tutorials.actors',
    user_model=None) 
SECRET_KEY = "20227" # see :djangoticket:`20227`
