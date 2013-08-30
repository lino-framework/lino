from lino.ui import Site
SITE = Site(globals(),
    'tutorials.de_BE',
    user_model=None,
    languages=['en','de','de-be']) 
SECRET_KEY = "20227" # see :djangoticket:`20227`
