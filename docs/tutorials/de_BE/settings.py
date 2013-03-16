from lino.ui import Site
SITE = Site(__file__,globals(),
    'tutorials.de_BE',
    user_model=None,
    languages=['en','de','de-be']) 
