# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Defines entry fields for IBAN and BIC.
"""

from django.db import models

from localflavor.generic import models as iban_fields

from django.utils.six import with_metaclass

from lino.api import dd

from lino.utils.jsgen import js_code
from lino.modlib.extjs.elems import CharFieldElement


class UppercaseTextFieldElement(CharFieldElement):
    """A CharFieldElement which accepts only upper-case characters.
    """
    value_template = "new Lino.UppercaseTextField(%s)"


class IBANFieldElement(UppercaseTextFieldElement):
    def get_column_options(self, **kw):
        """Return a string to be used as `Ext.grid.Column.renderer
        <http://docs.sencha.com/extjs/3.4.0/#!/api/Ext.grid.Column-cfg-renderer>`.

        """
        kw = super(
            UppercaseTextFieldElement, self).get_column_options(**kw)
        kw.update(renderer=js_code('Lino.iban_renderer'))
        return kw


class UppercaseTextField(with_metaclass(
        models.SubfieldBase, models.CharField, dd.CustomField)):
    """A custom CharField that accepts only uppercase caracters."""
    def create_layout_elem(self, *args, **kw):
        return UppercaseTextFieldElement(*args, **kw)

    def to_python(self, value):
        if isinstance(value, basestring):
            return value.upper()
        return value


class BICField(with_metaclass(
        models.SubfieldBase, iban_fields.BICField, UppercaseTextField)):
    """Database field used to store a BIC. """


class IBANField(with_metaclass(
        models.SubfieldBase, iban_fields.IBANField, dd.CustomField)):
    """Database field used to store an IBAN. """

    def create_layout_elem(self, *args, **kw):
        return IBANFieldElement(*args, **kw)

    def to_python(self, value):
        if isinstance(value, basestring):
            return value.upper().replace(' ', '')
        return value

    # def get_column_renderer(self):
    #     return 'Lino.iban_renderer'


