# -*- coding: UTF-8 -*-
# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)
"""

Default data for `pages` is the content defined in 
:mod:`lino.modlib.pages.fixtures.web`.

"""
#~ from lino.modlib.pages.fixtures.web import objects


def objects():

    from lino.modlib.pages.fixtures.intro import objects
    yield objects()

    #~ from lino.modlib.pages.fixtures.man import objects
    #~ yield objects()
