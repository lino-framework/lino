# -*- coding: UTF-8 -*-
"""

"""
from __future__ import unicode_literals
from __future__ import print_function

from lino.api import rt, dd


def objects():
    SessionType = rt.modules.clocking.SessionType
    ServiceReport = rt.modules.clocking.ServiceReport
    yield SessionType(id=1, name="Default")

    ExcerptType = rt.modules.excerpts.ExcerptType
    kw = dict(
        body_template='default.body.html',
        print_recipient=False,
        primary=True, certifying=True)
    kw.update(dd.str2kw('name', ServiceReport._meta.verbose_name))
    yield ExcerptType.update_for_model(ServiceReport, **kw)
