# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""This is the traditional Django URLConf module used by
:mod:`lino_noi.settings.public`.

"""

from django.conf import settings
from django.conf.urls import include, url

from . import views

from lino.api import rt

settings.SITE.startup()

urlpatterns = [
    url(r'^$',
        views.Index.as_view(),
        name='index'),
    url(r'^ticket/(?P<pk>[0-9]+)/$',
        views.Detail.as_view(model=rt.modules.tickets.Ticket)),
    url('', include('lino.core.urls'))
]


