# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

# class UppercaseFieldElement(CharFieldElement):
#     def get_field_options(self, **kw):
#         kw = super(UppercaseFieldElement, self).get_field_options(**kw)
#         kw.update(style='text-transform:uppercase;')
#         return kw

from django.db import models

from django_iban import fields as iban_fields

from django.utils.six import with_metaclass

from lino import dd, rt

from lino.utils.jsgen import js_code
from lino.ui.elems import CharFieldElement


class UppercaseTextFieldElement(CharFieldElement):
    """A CharFieldElement which accepts only upper-case characters.
    """
    value_template = "new Lino.UppercaseTextField(%s)"


class IBANFieldElement(UppercaseTextFieldElement):
    def get_column_options(self, **kw):
        """Return a string to be used as
`ext.grid.Column.renderer
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
        models.SubfieldBase, iban_fields.SWIFTBICField, UppercaseTextField)):
    pass


class IBANField(with_metaclass(
        models.SubfieldBase, iban_fields.IBANField, dd.CustomField)):

    def create_layout_elem(self, *args, **kw):
        return IBANFieldElement(*args, **kw)

    def to_python(self, value):
        if isinstance(value, basestring):
            return value.upper().replace(' ', '')
        return value

    # def get_column_renderer(self):
    #     return 'Lino.iban_renderer'


