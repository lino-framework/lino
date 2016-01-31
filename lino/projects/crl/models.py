# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _


from lino.api import dd, rt
from lino.modlib.countries import models as countries
from lino.modlib.contacts import models as contacts

from lino.utils import str2hex, hex2str


class CRL(str):

    """\
A `Concise Reference Label`
    """
    pass


class CrlField(models.CharField):

    """A field that contains a Concise Reference Label.
CRL fields need to be sorted using pure ASCII sequence. 
Since this is not a database-transparent feature in Django, 
we store these strings as their hexadecimal representation.
    """

    def __init__(self, *args, **kw):
        defaults = dict(
            verbose_name=_("Label"),
            max_length=100,
            blank=True,
        )
        defaults.update(kw)
        models.CharField.__init__(self, *args, **defaults)

    def from_db_value(self, value, expression, connection, context):
        return CRL(hex2str(value)) if value else ''

    def to_python(self, value):
        if not value:
            return value
        if isinstance(value, CRL):
            return value
        return CRL(hex2str(value))

    def get_prep_value(self, value):
        if not value:
            return value
        assert isinstance(value, CRL)
        return str2hex(value)


dd.inject_field(countries.Place, 'crl', CrlField())
dd.inject_field(contacts.Person, 'crl', CrlField())
dd.inject_field(contacts.Person, 'died_date',
                models.DateField(
                    blank=True, null=True,
                    verbose_name=_("Died date")))
dd.inject_field(contacts.Company, 'crl', CrlField())
