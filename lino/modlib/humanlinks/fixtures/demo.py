# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.
"""
The `demo` fixture for `humanlinks`
===================================

Creates a fictive family tree.

"""


from lino.utils.instantiator import Instantiator
from lino import dd

Person = dd.modules.contacts.Person
Link = dd.modules.humanlinks.Link
LinkTypes = dd.modules.humanlinks.LinkTypes


class InstanceGenerator(object):
    def __init__(self):
        self._objects = []
        self._instantiators = dict()

    def add_instantiator(self, *args, **kw):
        i = Instantiator(*args, **kw)
        # self._instantiators[i.model] = i
        k = i.model.__name__.lower()

        def f(*args, **kw):
            o = i.build(*args, **kw)
            self._objects.append(o)
            return o
        setattr(self, k, f)

    def flush(self):
        rv = self._objects
        self._objects = []
        return rv


NAME1 = "Frisch"


def objects():

    ig = InstanceGenerator()
    ig.add_instantiator(Person, 'first_name last_name gender birth_date')
    ig.add_instantiator(Link, 'parent child type')

    opa = ig.person("Hubert", NAME1, 'M', '1933-07-21')
    oma = ig.person("Gaby", "Frogemuth", 'F', '1934-08-04')

    P = ig.person("Paul", NAME1, 'M', '1967-06-19')
    L = ig.person("Ludwig", NAME1, 'M', '1968-06-01')
    A = ig.person("Alice", NAME1, 'F', '1969-12-19')
    B = ig.person("Bernd", NAME1, 'M', '1971-09-10')

    P1 = ig.person("Paula", "Einzig", 'F', '1968-12-19')
    P1A = ig.person("Peter", NAME1, 'M', '1987-06-19')
    P2 = ig.person("Petra", "Zweith", 'F', '1968-12-19')
    P2A = ig.person("Philippe", NAME1, 'M', '1997-06-19')
    P2B = ig.person("Clara", NAME1, 'F', '1999-06-19')
    P3 = ig.person("Dora", "Drosson", 'F', '1971-12-19')
    P3A = ig.person("Dennis", NAME1, 'M', '2001-06-19')

    yield ig.flush()

    ig.link(opa, oma, LinkTypes.spouse)

    for i in (P, L, A, B):
        ig.link(opa, i, LinkTypes.parent)
        ig.link(oma, i, LinkTypes.parent)

    ig.link(P, P1A, LinkTypes.parent)
    ig.link(P1, P1A, LinkTypes.parent)

    ig.link(P, P2A, LinkTypes.parent)
    ig.link(P2, P2A, LinkTypes.parent)

    ig.link(P, P2B, LinkTypes.parent)
    ig.link(P2, P2B, LinkTypes.parent)

    ig.link(P, P3A, LinkTypes.parent)
    ig.link(P3, P3A, LinkTypes.parent)

    ig.link(P, P2, LinkTypes.spouse)

    yield ig.flush()
