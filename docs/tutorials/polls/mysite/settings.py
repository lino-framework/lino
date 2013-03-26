from lino.projects.std.settings import Site
SITE = Site(__file__,globals(),'polls',title="Cool Polls")
# your local settings here
DEBUG = True
# DATABASES = ...
SECRET_KEY = 'abc123'
