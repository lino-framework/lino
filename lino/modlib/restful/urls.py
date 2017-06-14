# Originally copied from :mod:`rest_framework.urls`.
"""
Login and logout views for the browsable API.

Add these to your root URLconf if you're using the browsable API and
your API requires authentication::

    urlpatterns = [
        ...
        url(r'^auth/', include('lino.modlib.restful.urls', namespace='rest_framework'))
    ]

In Django versions older than 1.9, the urls must be namespaced as 'rest_framework',
and you should make sure your authentication settings include `SessionAuthentication`.
"""
from __future__ import unicode_literals

from django.conf.urls import url, include

# urlpatterns = [
#     url(r'^api-auth/', include('rest_framework.urls',
#                                namespace='rest_framework')),
# ]
# RuntimeError: Model class django.contrib.auth.models.Permission doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.


# from django.contrib.auth import views
# from lino.modlib.users import views


# template_name = {'template_name': 'rest_framework/login.html'}

# app_name = 'rest_framework'
# urlpatterns = [
#     url(r'^login/$', views.login, template_name, name='login'),
#     url(r'^logout/$', views.logout, template_name, name='logout'),
# ]

