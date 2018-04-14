# -*- coding: UTF-8 -*-
# Copyright 2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _


def objects():

    if not dd.is_installed('excerpts'):
        return
    if not dd.is_installed('appypod'):
        return

    ContentType = rt.models.contenttypes.ContentType
    ExcerptType = rt.models.excerpts.ExcerptType

    yield ExcerptType(
        build_method='appyodt',
        #template='Default.odt',
        body_template='welcome.body.html',
        # certifying=True,
        primary=True,
        content_type=ContentType.objects.get_for_model(
            rt.models.users.User),
        **dd.str2kw('name', _("Welcome letter")))

