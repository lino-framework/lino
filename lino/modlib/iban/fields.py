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

# class UppercaseFieldElement(CharFieldElement):
#     def get_field_options(self, **kw):
#         kw = super(UppercaseFieldElement, self).get_field_options(**kw)
#         kw.update(style='text-transform:uppercase;')
#         return kw

from django.db import models

from django_iban import fields as iban_fields

from lino import dd

from lino.ui.elems import CharFieldElement


class UppercaseTextFieldElement(CharFieldElement):
    """A CharFieldElement which accepts only upper-case characters.
    """
    value_template = "new Lino.UppercaseTextField(%s)"


class UppercaseTextField(models.CharField, dd.CustomField):
    """A custom CharField that accepts only uppercase caracters."""
    def create_layout_elem(self, *args, **kw):
        return UppercaseTextFieldElement(*args, **kw)

    def to_python(self, value):
        if isinstance(value, basestring):
            return value.upper()


class IBANField(iban_fields.IBANField, UppercaseTextField):
    pass


class BICField(iban_fields.SWIFTBICField, UppercaseTextField):
    pass

