from lino import Site
SITE = Site(__file__,globals())
INSTALLED_APPS = [ 'lino.test_apps.integer_pk','lino','django_site']
