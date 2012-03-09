## Copyright 2011-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

r"""
A shortcut to classes and methods needed 
when defining your database structure in a `models` module.
The name "dd" stands for "Data Definition". 

Tables:

- :class:`Table <lino.core.table.Table>`
- :class:`VirtualTable <lino.utils.tables.VirtualTable>`
- :class:`Frame <lino.core.actors.Frame>`
- :class:`EmptyTable <lino.core.actors.EmptyTable>`


Extended Fields:

- :class:`IncompleteDateField <lino.core.fields.IncompleteDateField>`
- :class:`PasswordField <lino.core.fields.PasswordField>`
- :class:`MonthField <lino.core.fields.MonthField>`
- :class:`QuantityField <lino.core.fields.QuantityField>`
- :class:`PriceField<lino.core.fields.PriceField>`
- :class:`GenericForeignKey <lino.core.fields.GenericForeignKey>`
- :class:`GenericForeignKeyIdField <lino.core.fields.GenericForeignKeyIdField>`

Virtual Fields:

- :class:`Constant <lino.core.fields.Constant>` and 
  :class:`@constant <lino.core.fields.constant>`
- :class:`DisplayField <lino.core.fields.DisplayField>` and 
  :class:`@displayfield <lino.core.fields.displayfield>`
- :class:`VirtualField <lino.core.fields.VirtualField>` and
  :class:`@virtualfield <lino.core.fields.virtualfield>`
  

Utilities:

- :func:`resolve_field <lino.tools.resolve_field>`
- :func:`resolve_model <lino.tools.resolve_model>`
- :func:`get_app <lino.tools.get_app>`


"""


from lino.utils.tables import VirtualTable
#~ from lino.utils.tables import computed
#~ from lino.utils.tables import ComputedColumn

from lino.tools import resolve_model, get_app, resolve_field, get_field

#~ from lino.core.table import fields_list, inject_field
from lino.core.table import has_fk
from lino.core.table import Table
#~ from lino.core import table
#~ Table = table.Table

from lino.core.table import summary, summary_row

from lino.core.actors import Frame
from lino.core.actors import EmptyTable

from lino.core.actions import RowAction
from lino.core.actions import GridEdit, ShowDetailAction
from lino.core.actions import InsertRow, DeleteSelected
from lino.core.actions import SubmitDetail, SubmitInsert
from lino.core.actions import Calendar

from lino.core.fields import GenericForeignKey
from lino.core.fields import GenericForeignKeyIdField
from lino.core.fields import IncompleteDateField
from lino.core.fields import PasswordField
from lino.core.fields import MonthField
from lino.core.fields import LinkedForeignKey
from lino.core.fields import QuantityField
from lino.core.fields import HtmlBox, PriceField, RichTextField

from lino.core.fields import DisplayField, displayfield
from lino.core.fields import VirtualField, virtualfield
from lino.core.fields import RequestField, requestfield
from lino.core.fields import Constant, constant
#~ from lino.core.fields import MethodField

from lino.utils import perms

from lino.core.layouts import DetailLayout


class Module(object):
    pass
    
def fields_list(model,field_names):
    """
    Return a list with the names of the specified fields, 
    checking whether each of them exists.
    
    Arguments: 
    `model` is any subclass of `django.db.models.Model`.
    `field_names` is a single string with a space-separated list of field names.
    
    For example if you have a model `MyModel` 
    with two fields `foo` and `bar`,
    then ``dd.fields_list(MyModel,"foo bar")`` 
    will return ``['foo','bar']``
    and ``dd.fields_list(MyModel,"foo baz")`` will raise an exception.
    """
    #~ return tuple([get_field(model,n) for n in field_names.split()])
    #~ if model.__name__ == 'Company':
        #~ print 20110929, [get_field(model,n) for n in field_names.split()]
    return [get_field(model,n).name for n in field_names.split()]

    
def inject_field(model,name,field,doc=None):
    """
    Adds the given field to the given model.
    See also :doc:`/tickets/49`.
    """
    #~ model = resolve_model(model)
    if doc:
        field.__doc__ = doc
    model.add_to_class(name,field)
    return field

def update_field(model,name,**kw):
    """
    Update some attribute of the specified existing field.
    For example 
    :class:`PersonMixin <lino.modlib.contacts.models.PersonMixin>` 
    defines a field `first_name` which may not be blank.
    If you inherit from 
    :class:`PersonMixin <lino.modlib.contacts.models.PersonMixin>`
    but want `first_name` to be optional::
    
      class MyPerson(contacts.PersonMixin):
        ...
      dd.update_field(MyPerson,'first_name',blank=True)
    
    """
    fld = model._meta.get_field_by_name(name)[0]
    for k,v in kw.items():
        setattr(fld,k,v)
        

