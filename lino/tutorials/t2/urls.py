from django.conf.urls.defaults import patterns, include, url

from lino.ui.extjs3 import UI

# install Lino urls under root location (`/`)
urlpatterns = UI().get_patterns()
