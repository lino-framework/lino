from lino.projects.std.settings import Site
SITE = Site(__file__,globals(),'polls',title="Cool Polls",no_local=True)
# your local settings here
DEBUG = True
# DATABASES = ...