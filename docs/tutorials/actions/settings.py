from lino.ui import Site
SITE = Site(globals(),
    'tutorials.actions',
    user_model=None) 
SECRET_KEY = "20227" # see :djangoticket:`20227`
