# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)


def objects():

    from lino.history import blogger
    yield blogger.flush()

    import lino.history.luc201212
    yield blogger.flush()
