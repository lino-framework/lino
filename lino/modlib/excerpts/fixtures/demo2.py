# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Makes sure that there is at least one excerpt for every ExcerptType.
Render all excerpts by running their do_print method.

"""

from lino.api import rt, dd


def objects():
    ExcerptType = rt.modules.excerpts.ExcerptType
    Excerpt = rt.modules.excerpts.Excerpt

    if not dd.plugins.excerpts.responsible_user:
        return

    ses = rt.login(dd.plugins.excerpts.responsible_user)

    for et in ExcerptType.objects.all():
        if Excerpt.objects.filter(excerpt_type=et).count() == 0:
            model = et.content_type.model_class()
            qs = model.objects.all()
            if qs.count() > 0:
                ses.selected_rows = [qs[0]]
                yield et.get_or_create_excerpt(ses)

    for obj in Excerpt.objects.all():
        # dd.logger.info("20150526 rendering %s", obj)
        rv = ses.run(obj.do_print)
        assert rv['success']

