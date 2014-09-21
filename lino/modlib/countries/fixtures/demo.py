# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)


def objects():
    from lino.modlib.countries.fixtures.few_countries import objects
    yield objects()
    from lino.modlib.countries.fixtures.few_cities import objects
    yield objects()
