# -*- coding: UTF-8 -*-
# Copyright 2014-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Creates a certifying :class:`ExcerptType` instance for every model
which inherits from :class:`Certifiable`.

"""

from django.contrib.contenttypes.models import ContentType

from lino.api import dd, rt
from lino.modlib.excerpts.mixins import Certifiable


def objects():
    ExcerptType = rt.modules.excerpts.ExcerptType
    for cls in rt.models_by_base(Certifiable):
        kw = dd.str2kw('name', cls._meta.verbose_name)
        if False:
            kw.update(backward_compat=True)
        yield ExcerptType(
            #template='Default.odt',
            primary=True,
            certifying=True,
            content_type=ContentType.objects.get_for_model(cls),
            **kw)

