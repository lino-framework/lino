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

A small wrapper around Django's `Model` class 
which adds some Lino specific features:

- :class:`Model <lino.core.modeltools.Model>`

Tables:

- :class:`Table <lino.core.table.Table>`
- :class:`VirtualTable <lino.utils.tables.VirtualTable>`
- :class:`Frame <lino.core.frames.Frame>`

Extended Fields:

- :class:`IncompleteDateField <lino.core.fields.IncompleteDateField>`
- :class:`PasswordField <lino.core.fields.PasswordField>`
- :class:`MonthField <lino.core.fields.MonthField>`
- :class:`QuantityField <lino.core.fields.QuantityField>`
- :class:`PriceField<lino.core.fields.PriceField>`
- :class:`GenericForeignKey <lino.core.fields.GenericForeignKey>`
- :class:`GenericForeignKeyIdField <lino.core.fields.GenericForeignKeyIdField>`
- :class:`RecurrenceField <lino.core.fields.RecurrenceField>`
- :class:`DummyField <lino.core.fields.DummyField>`

Babel fields:

- :class:`BabelCharField <lino.utils.babel.BabelCharField>`
- :class:`BabelTextField <lino.utils.babel.BabelTextField>`

Virtual Fields:

- :class:`Constant <lino.core.fields.Constant>` and 
  :class:`@constant <lino.core.fields.constant>`
- :class:`DisplayField <lino.core.fields.DisplayField>` and 
  :class:`@displayfield <lino.core.fields.displayfield>`
- :class:`VirtualField <lino.core.fields.VirtualField>` and
  :class:`@virtualfield <lino.core.fields.virtualfield>`
- :class:`HtmlBox <lino.core.fields.HtmlBox>`

Layouts:

- :class:`FormLayout <lino.core.layouts.FormLayout>`
  
Utilities:

- :func:`resolve_field <lino.core.modeltools.resolve_field>`
- :func:`resolve_model <lino.core.modeltools.resolve_model>`
- :func:`resolve_app <lino.core.modeltools.resolve_app>` 
- :func:`chooser <lino.utils.choosers.chooser>` 

Miscellaneous:

- :class:`UserProfiles <lino.utils.perms.UserProfiles>`
- :class:`UserGroups <lino.utils.perms.UserGroups>`
- :class:`UserLevels <lino.utils.perms.UserLevels>`


"""

import logging
logger = logging.getLogger(__name__)


from lino.utils.tables import VirtualTable
#~ from lino.utils.tables import computed
#~ from lino.utils.tables import ComputedColumn

from lino.core.modeltools import resolve_model, resolve_app, resolve_field, get_field, UnresolvedModel
from lino.core.modeltools import Model

#~ from lino.core.table import fields_list, inject_field
from lino.core.table import has_fk
from lino.core.table import Table
from django.db.models.fields import FieldDoesNotExist
from django.db import models
#~ Model = models.Model
#~ from lino.core import table
#~ Table = table.Table

from lino.core.table import summary, summary_row

from lino.core.frames import Frame
#~ from lino.core.frames import EmptyTable

from lino.core.actions import action
from lino.core.actions import RowAction
from lino.core.actions import GridEdit, ShowDetailAction
from lino.core.actions import InsertRow, DeleteSelected
from lino.core.actions import SubmitDetail, SubmitInsert
from lino.core.actions import Calendar

from lino.core.fields import DummyField
from lino.core.fields import RecurrenceField
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
from lino.utils.babel import BabelCharField, BabelTextField
#~ from lino.core.fields import MethodField

from lino.utils.choosers import chooser

#~ from lino.utils.perms import UserLevels, UserProfiles
from lino.utils.perms import UserLevels, UserGroups, UserProfiles

from lino.core.layouts import FormLayout
#~ DetailLayout = InsertLayout = FormLayout

#~ from lino.core.layouts import DetailLayout, InsertLayout


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


PENDING_INJECTS = dict()
PREPARED_MODELS = dict()

def on_class_prepared(signal,sender=None,**kw):
    model = sender
    #~ return
    #~ if model is None:
        #~ return 
    k = model._meta.app_label + '.' + model.__name__
    PREPARED_MODELS[k] = model
    #~ logger.info("20120627 on_class_prepared %r = %r",k,model)
    injects = PENDING_INJECTS.pop(k,None)
    if injects is not None:
        for f in injects:
            f(model)
        #~ for k,v in injects.items():
            #~ model.add_to_class(k,v)
            
models.signals.class_prepared.connect(on_class_prepared)

def inject_field(model_spec,name,field,doc=None):
    """
    Adds the given field to the given model.
    See also :doc:`/tickets/49`.
    """
    if doc:
        field.__doc__ = doc
    #~ model = resolve_model(model,strict=True)
    def todo(model):
        model.add_to_class(name,field)
    #~ model = resolve_model(model_spec,seed_cache=False)
    if isinstance(model_spec,basestring):
        k = model_spec
        model = PREPARED_MODELS.get(k,None)
    else:
        model = model_spec
        k = model._meta.app_label + '.' + model.__name__
    #~ if isinstance(model,UnresolvedModel): 
    if model is None: 
        injects = PENDING_INJECTS.setdefault(k,[])
        injects.append(todo)
        #~ d[name] = field
        #~ logger.info("20120627 Defer inject_field(%r,%r,%r)", model_spec,name,field)
        return
    todo(model)
    #~ return field

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
    try:
        fld = model._meta.get_field_by_name(name)[0]
    except FieldDoesNotExist:
        logger.warning("Cannot update unresolved field %s.%s", model,name)
        return
        return
    for k,v in kw.items():
        setattr(fld,k,v)
        

def inject_quick_add_buttons(model,name,target):
    """
    Injects a virtual display field `name` into the specified `model`.
    This field will show up to three buttons
    `[New]` `[Show last]` `[Show all]`. 
    `target` is the table that will run these actions.
    It must be a slave of `model`.
    """
    def fn(self,rr):
        return rr.renderer.quick_add_buttons(
          rr.spawn(target,master_instance=self))
    inject_field(model,name,
        VirtualField(DisplayField(
            target.model._meta.verbose_name_plural),fn))
    
def add_user_group(name,label):
    """
    Add a user group to the :class:`UserGroups <lino.utils.perms.UserGroups>` 
    choicelist. If a group with that name already exists, add `label` to the 
    existing group.
    """
    #~ logging.info("add_user_group(%s,%s)",name,label)
    #~ print "20120705 add_user_group(%s,%s)" % (name,unicode(label))
    g = UserGroups.items_dict.get(name)
    if g is None:
        UserGroups.add_item(name,label)
    else:
        if g.text != label:
            g.text += " & " + unicode(label)
    
