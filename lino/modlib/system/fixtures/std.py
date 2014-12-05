# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from django.conf import settings
from lino.utils.instantiator import Instantiator


def objects():
    if settings.SITE.user_model:
        tft = Instantiator('system.TextFieldTemplate',
                           "name description text").build

        yield tft("hello", "Inserts 'Hello, world!'", """<div>Hello, world!</div>""")
        #~ yield tft("mfg","",'<p>Mit freundlichen Gr&uuml;&szlig;en<br><p class="data_field">root</p>')
        yield tft("mfg", "", '<p>Mit freundlichen Gr&uuml;&szlig;en<br><p>{{request.subst_user or request.user}}</p>')

