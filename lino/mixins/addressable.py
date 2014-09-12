# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
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
Used by :class:`lino.utils.appy_pod.PrintLabelsAction` and 
:mod:`lino.modlib.contacts`.

"""

from __future__ import print_function

from lino.utils import join_elems
from lino.utils.xmlgen.html import E


class Addressable(object):
    "See :class:`dd.Addressable`."
    def address_person_lines(self):
        raise NotImplementedError()

    def address_location_lines(self):
        raise NotImplementedError()

    def address_lines(self):
        for ln in self.address_person_lines():
            yield ln
        for ln in self.address_location_lines():
            yield ln

    def get_address(self, linesep="\n"):
        #~ return linesep.join(self.address_lines())
        return linesep.join(list(self.address_person_lines()) + list(self.address_location_lines()))
    address = property(get_address)

    def get_address_html(self, **attrs):
        """
        """
        lines = join_elems(self.address_lines(), E.br)
        return E.tostring(E.p(*lines, **attrs))

    address_html = property(get_address_html)
