# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Used by :class:`lino.utils.appy_pod.PrintLabelsAction` and
:mod:`ml.contacts`.

$ python setup.py test -s tests.UtilsTests.test_addressable

"""

from __future__ import print_function

from lino.utils.xmlgen.html import E, lines2p


class Addressable(object):
    """Mixin to encapsulate the generating of "traditional" ("snail") mail
    addresses.

    It differentiates between the "person" and the "location" part of
    an address.  For example::
    
        Mr. Luc Saffre     | person
        Rumma & Ko OÜ      | person
        Uus 1              | location
        Vana-Vigala küla   | location
        Vigala vald        | location
        Estonia            | location

    .. attribute:: address

        A property which calls :meth:`get_address`.

    .. attribute:: address_html

        A property which calls :meth:`get_address_html`.

    """
    def address_person_lines(self):
        """Expected to yield one or more unicode strings, one for each line
        of the person part.

        """
        raise NotImplementedError()

    def address_location_lines(self):
        """Expected to yield one or more unicode strings, one for each line
        of the location part.

        """
        raise NotImplementedError()

    def get_address_lines(self):
        for ln in self.address_person_lines():
            yield ln
        for ln in self.address_location_lines():
            yield ln

    def get_address(self, linesep="\n"):
        """The plain text full postal address (person and location).  Lines
        are separated by `linesep` which defaults to a newline.
        """
        return linesep.join(
            list(self.address_person_lines())
            + list(self.address_location_lines()))
    address = property(get_address)

    def get_address_html(self, *args, **kwargs):
        """Returns the full postal address a a string containing html
        markup of style::
        
            <p>line1<br/>line2...</p>

        If `min_height` is specified, makes sure that the string
        contains at least that many lines. Adds as many empty lines
        (``<br/>``) as needed.  This is useful in a template which
        wants to get a given height for every address.
          
        Optional attributes for the enclosing `<p>` tag can be
        specified as keyword arguments. Example::

            >>> class MyAddr(Addressable):
            ...     def __init__(self, *lines): self.lines = lines
            ...     def address_person_lines(self): return []
            ...     def address_location_lines(self): return self.lines
            ...     
            >>> addr = MyAddr('line1', 'line2')
            >>> print(addr.get_address_html(class_="Recipient"))
            <p class="Recipient">line1<br />line2</p>
          
        This is done using the :func:`lino.utils.xmlgen.html.lines2p`
        function (see there for more examples).

        """
        lines = list(self.get_address_lines())
        return E.tostring(lines2p(lines, *args, **kwargs))

    address_html = property(get_address_html)


