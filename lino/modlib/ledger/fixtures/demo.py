# -*- coding: UTF-8 -*-
# Copyright 2009-2013 Luc Saffre
# License: BSD (see file COPYING for details)


def objects():
    # cannot use relative imports here because dpy uses low-level
    # `__import__()'
    from lino.modlib.ledger.fixtures import mini
    yield mini.objects()

    #~ from lino.modlib.ledger.fixtures import demo_bookings
    #~ yield demo_bookings.objects()
