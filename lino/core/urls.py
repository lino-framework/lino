# Copyright 2009-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The default URLconf module for Lino applications.
As an application developer you don't need to worry about this.

This is found by Django because :mod:`lino.projects.std.settings`
:setting:`ROOT_URLCONF` is set to :mod:`lino.core.urls`.

"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from lino.core.utils import is_devserver

# we must explicitly call django.setup() because when running under
# mod_wsgi this is not done automatically as with runserver (or at
# least it seems so)
import lino
lino.startup()


site = settings.SITE
urlpatterns = []

if site.site_prefix:
    prefix = site.site_prefix[1:]
else:
    prefix = ''
rx = '^' + prefix

for p in site.installed_plugins:
    pat = p.get_patterns()
    prx = rx
    if p.url_prefix:
        prx += p.url_prefix + "/"
    if prx == '^':
        urlpatterns += pat
    else:
        urlpatterns.append(url(prx, include(pat)))

if site.social_auth_backends:
    urlpatterns.append(
        url('^oauth/', include('social_django.urls', namespace='social')))
        
        

if site.django_admin_prefix:  # not tested
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns.append(url(
        rx + site.django_admin_prefix[1:]
        + "/", include(admin.site.urls)))

#~ logger.info("20130409 is_devserver() returns %s.",is_devserver())
if is_devserver():
    # from django.contrib.staticfiles.views import serve
    # opts = {'document_root': settings.MEDIA_ROOT,
    #         'show_indexes': False}
    # pat = r'^%s(?P<path>.*)$' % prefix
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        # 'django.views.static', (pat, 'serve', opts))
    # print('\n'.join(map(str, lst)))
    # print(20171212, lst)
    # why do i need the following? i thought that this is done
    # automatically:
    # urlpatterns += static(
    #     settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # logger.info("20150426 serve static %s -> %s",
    #             settings.STATIC_URL, settings.STATIC_ROOT)

    # pat = r'^{0}(?P<path>.*)$'.format(settings.STATIC_URL[1:])
    # urlpatterns.append(url(pat, serve))
