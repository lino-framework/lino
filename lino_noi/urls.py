from lino.api import dd


# urlpatterns = dd.plugins.bootstrap3.get_patterns(None)


from django.conf import settings
from django.conf.urls import include, url

from . import views

from lino.api import rt

settings.SITE.startup()

urlpatterns = settings.SITE.kernel.get_patterns()

urlpatterns += [
    # ex: /polls/
    url(r'^$',
        views.Index.as_view(),
        name='index'),
    # ex: /polls/5/
    url(r'^ticket/(?P<pk>[0-9]+)/$',
        views.Detail.as_view(model=rt.modules.tickets.Ticket)),
    # url(r'^(?P<pk>[0-9]+)/$',
    #     views.Detail.as_view(model=rt.modules.contacts.Person),
    #     name='detail'),
    # ex: /polls/5/results/
    # url(r'^(?P<company_id>[0-9]+)/contacts/$',
    #     views.contacts, name='contacts'),
]

# urlpatterns += [
#     url(r'^admin/', include('lino.core.urls')),
# ]



