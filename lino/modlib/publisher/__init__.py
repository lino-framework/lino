# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api.ad import Plugin


class Plugin(Plugin):

    needs_plugins = ["lino.modlib.jinja"]

    def get_patterns(self):
        from django.conf.urls import url
        from lino.core.utils import models_by_base
        from . import views
        from .mixins import Publishable

        for m in models_by_base(Publishable):
            if m.publisher_location is not None:
                yield url('^{}/(?P<pk>.+)$'.format(m.publisher_location),
                    views.Element.as_view(publisher_model=m))
