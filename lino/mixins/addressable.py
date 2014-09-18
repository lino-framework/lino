# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

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
