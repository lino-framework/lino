
from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required

from django.contrib import admin
admin.autodiscover()

#from lino.django.nodes import views

urlpatterns = patterns('',
    (r'^(.*)$', admin.site.root),
    (r'^db/(.*)', login_required(databrowse.site.root)),
)    

#~ urlpatterns = patterns('',
    #~ (r'^$', views.index),
    #~ (r'^nodes/', include('lino.django.nodes.urls')),
    #~ (r'^polls/', include('lino.django.polls.urls')),
    #~ (r'^contacts/', include('lino.django.contacts.urls')),
    #~ (r'^admin/(.*)', admin.site.root),
    #~ (r'^db/(.*)', login_required(databrowse.site.root)),
    #~ # (r'^.*$', nodes.views.index),
#~ )


#~ urlpatterns += patterns('',
    #~ (r'^accounts/login/$', 'django.contrib.auth.views.login'),
#~ )                        

