# -*- coding: UTF-8 -*-
# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)

u"""
Tools for generating  
`Belgian Intervat declarations
<http://minfin.fgov.be/portail2/fr/e-services/intervat/>`_

>>> vat_number = "0123456789"
>>> def me():
...   return (
...      iic.Name("Foo, Bar & Baz"),
...      iic.Street(u"rue de l'école 57"),
...      iic.PostCode(u"4000"),
...      iic.City(u"Liège"),
...      iic.CountryCode("BE"),
...      iic.EmailAddress("foo@barbaz.be"),
...      iic.Phone("02345678")
...   )
>>> root = clc.ClientListingConsignment(
...   clc.Representative(
...      iic.RepresentativeID(vat_number,issuedBy="BE",identificationType="TIN"),
...      *me()),
...   clc.ClientListing(
...     clc.Declarant(
...       iic.VATNumber(vat_number),
...       *me()),
...     clc.Period('2011'),
...     SequenceNumber=1,ClientsNbr=1,
...     TurnOverSum="1000.00",VATAmountSum="210.00"),
...   ClientListingsNbr=1)

>>> clc.validate_root(root)

Note that it validates although there are no clients but a sum.
That's because validate checks only the "syntax", not the "content".

>>> print etree.tostring(root,pretty_print=True) #doctest: +ELLIPSIS
<clc:ClientListingConsignment ... ClientListingsNbr="1">
  <clc:Representative>
    <iic:RepresentativeID identificationType="TIN" issuedBy="BE">0123456789</iic:RepresentativeID>
    <iic:Name>Foo, Bar &amp; Baz</iic:Name>
    <iic:Street>rue de l'&#233;cole 57</iic:Street>
    <iic:PostCode>4000</iic:PostCode>
    <iic:City>Li&#232;ge</iic:City>
    <iic:CountryCode>BE</iic:CountryCode>
    <iic:EmailAddress>foo@barbaz.be</iic:EmailAddress>
    <iic:Phone>02345678</iic:Phone>
  </clc:Representative>
  <clc:ClientListing TurnOverSum="1000.00" ClientsNbr="1" VATAmountSum="210.00" SequenceNumber="1">
    <clc:Declarant>
      <iic:VATNumber>0123456789</iic:VATNumber>
      <iic:Name>Foo, Bar &amp; Baz</iic:Name>
      <iic:Street>rue de l'&#233;cole 57</iic:Street>
      <iic:PostCode>4000</iic:PostCode>
      <iic:City>Li&#232;ge</iic:City>
      <iic:CountryCode>BE</iic:CountryCode>
      <iic:EmailAddress>foo@barbaz.be</iic:EmailAddress>
      <iic:Phone>02345678</iic:Phone>
    </clc:Declarant>
    <clc:Period>2011</clc:Period>
  </clc:ClientListing>
</clc:ClientListingConsignment>
<BLANKLINE>

"""


import os

try:
    from lxml import etree
except ImportError:
    from lino.utils.xmlgen import etree

SubElement = etree.SubElement

from lino.utils import xmlgen as xg


def xsdpath(*parts):
    p1 = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(p1, 'XSD', *parts)


class IntervatInputCommon(xg.Namespace):
    xsd_filename = xsdpath('IntervatInputCommon_v0_7.xsd')
iic = IntervatInputCommon('iic')


class ClientListingConsignment(xg.Namespace):
    xsd_filename = xsdpath('NewLK-in_v0_7.xsd')
    used_namespaces = [iic]
clc = ClientListingConsignment('clc')


class IntraConsignment(xg.Namespace):
    xsd_filename = xsdpath('NewICO-in_v0_7.xsd')
    used_namespaces = [iic]
ico = IntraConsignment('ico')


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
