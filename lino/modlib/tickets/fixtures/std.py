# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Installs a primary certifiable ExcerptType for Milestone.

"""

from lino.api import rt, dd


def objects():
    Milestone = rt.modules.tickets.Milestone
    ExcerptType = rt.modules.excerpts.ExcerptType

    kw = dict(
        body_template='default.body.html',
        print_recipient=False,
        primary=True, certifying=True)
    kw.update(dd.str2kw('name', Milestone._meta.verbose_name))
    yield ExcerptType.update_for_model(Milestone, **kw)
