"""   
It is theoretically possible to install both Django's admin 
*and* Lino. 

But the details are left for those who are interested; 
Basically you just need to uncomment the related lines below.
But this still causes an ImproperlyConfigured error 
"Put 'django.contrib.auth.context_processors.auth' in 
your TEMPLATE_CONTEXT_PROCESSORS setting in order to 
use the admin application" (which is normal since 
we removed some settings needed by admin).

"""

from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# define non-Lino urls 
urlpatterns = patterns('',
    url(r'^$', 'lino.tutorials.t2.polls.views.index'))
    
# add /admin
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)))
    
    
# add Lino urls under `/lino` 
from lino.ui.extjs3 import UI
urlpatterns += UI('lino').get_patterns()
