# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Used by :class:`lino_xl.lib.appypod.PrintLabelsAction` and
:mod:`lino_xl.lib.contacts`.

.. How to test this:
    $ go book
    $ python setup.py test -s tests.test_utils.UtilsTests.test_addressable

"""

from etgen.html import E, lines2p, tostring


class Addressable(object):
    """General mixin (not only for Django models) to encapsulate the
    generating of "traditional" ("snail") mail addresses.

    It differentiates between the "person" and the "location" part of
    an address.  For example::

        Mr. Luc Saffre     | person
        Rumma & Ko OÜ      | person
        Uus 1              | location
        Vana-Vigala küla   | location
        Vigala vald        | location
        Estonia            | location

    Usable subclasses must implement at least
    :meth:`address_person_lines` and :meth:`address_location_lines`.

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
        """Yields a series of strings, one for each line of the address."""
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
        """Returns the full postal address as a string containing html
        markup of style::

            <p>line1<br/>line2...</p>

        This returns always exactly one paragraph, even if the address
        is empty (in which case the paragraph is empty):

        >>> print(TestAddress().get_address_html())
        <p/>

        Optional attributes for the enclosing `<p>` tag can be
        specified as keyword arguments. Example:

        >>> addr = TestAddress('line1', 'line2')
        >>> print(addr.get_address_html(**{'class':"Recipient"}))
        <p class="Recipient">line1<br/>line2</p>

        If `min_height` is specified, makes sure that the string
        contains at least that many lines. Adds as many empty lines
        (``<br/>``) as needed.  This is useful in a template which
        wants to get a given height for every address.

        >>> print(addr.get_address_html(min_height=5))
        <p>line1<br/>line2<br/><br/><br/></p>

        Any arguments are forwarded to :meth:`lines2p
        <etgen.html.lines2p>` which is used to pack the address
        lines into a paragraph (see there for more examples).

        """
        lines = list(self.get_address_lines())
        return tostring(lines2p(lines, *args, **kwargs))

    address_html = property(get_address_html)

    def has_address(self):
        """
        >>> TestAddress('line1', 'line2').has_address()
        True
        >>> TestAddress().has_address()
        False
        """
        return len(list(self.address_location_lines())) > 0


class TestAddress(Addressable):
    """Used only for testing."""
    def __init__(self, *lines):
        self.lines = lines

    def address_person_lines(self):
        return []

    def address_location_lines(self):
        return self.lines
