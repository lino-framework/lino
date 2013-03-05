## Copyright 2011-2013 Luc Saffre
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

"""
A shortcut to classes and methods needed 
when defining your database structure in a `models` module.

The name "dd" stands for "Data Definition".

A small wrapper around Django's `Model` class 
which adds some Lino specific features:

- :class:`Model <lino.core.model.Model>`

Tables:

- :class:`Table <lino.core.dbtables.Table>`
- :class:`VirtualTable <lino.core.tables.VirtualTable>`
- :class:`Frame <lino.core.frames.Frame>`

Extended Fields:

- :class:`EnableChild <lino.utils.mti.EnableChild>`
- :class:`NullCharField <lino.core.fields.NullCharField>`
- :class:`IncompleteDateField <lino.core.fields.IncompleteDateField>`
- :class:`PasswordField <lino.core.fields.PasswordField>`
- :class:`MonthField <lino.core.fields.MonthField>`
- :class:`PercentageField <lino.core.fields.PercentageField>`
- :class:`QuantityField <lino.core.fields.QuantityField>`
- :class:`PriceField<lino.core.fields.PriceField>`
- :class:`GenericForeignKey <lino.core.fields.GenericForeignKey>`
- :class:`GenericForeignKeyIdField <lino.core.fields.GenericForeignKeyIdField>`
- :class:`RecurrenceField <lino.core.fields.RecurrenceField>`
- :class:`DummyField <lino.core.fields.DummyField>`
- :func:`ForeignKey <lino.core.fields.ForeignKey>`

Multilingual database content:

- :class:`BabelNamed <north.babel.BabelNamed>`
- :class:`BabelCharField <north.babel.BabelCharField>`
- :class:`BabelTextField <fields.BabelTextField>`
- :class:`LanguageField <north.babel.LanguageField>`

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
- :class:`Panel <lino.core.layouts.Panel>`
  
Utilities:

- :func:`obj2str <django_site.modeltools.obj2str>`
- :func:`obj2unicode <django_site.modeltools.obj2unicode>`
- :func:`range_filter <django_site.modeltools.range_filter>`
- :func:`full_model_name <django_site.modeltools.full_model_name>`
- :func:`fields_list <lino.core.fields.fields_list>`
- :func:`resolve_field <lino.core.modeltools.resolve_field>`
- :func:`resolve_model <north.dbutils.resolve_model>`
- :func:`resolve_app <lino.core.modeltools.resolve_app>` 
- :func:`chooser <lino.utils.choosers.chooser>` 
- :func:`add_user_group` 
- :func:`update_field <lino.core.inject.update_field>` 
- :func:`inject_field <lino.core.inject.inject_field>` 
- :func:`inject_quick_add_buttons <lino.core.inject.inject_quick_add_buttons>` 

Signals:

- :attr:`startup <django_site.signals.startup>`
- :attr:`pre_analyze <lino.core.signals.pre_analyze>`
- :attr:`post_analyze <lino.core.signals.post_analyze>`
- :attr:`pre_merge <lino.core.signals.pre_merge>`
- :attr:`pre_ui_create <lino.core.signals.pre_ui_create>`
- :attr:`ChangeWatcher <lino.core.signals.ChangeWatcher>`
- :attr:`pre_ui_update <lino.core.signals.pre_ui_update>`
- :attr:`pre_ui_delete <lino.core.signals.pre_ui_delete>`
- :attr:`receiver <django.dispatch.receiver>` : the standard Django receiver decorator
- (and many more)

Actions:

- :class:`AuthorRowAction <lino.mixins.AuthorRowAction>`
- :class:`RowAction <lino.core.actions.RowAction>`
- :class:`AjaxAction <lino.core.actions.RowAction>`
- :class:`ChangeStateAction <lino.core.changes.ChangeStateAction>`
- :class:`NotifyingAction <lino.core.actions.NotifyingAction>`
- :class:`MergeAction <lino.core.merge.MergeAction>`

Miscellaneous:

- :class:`ChoiceList <lino.core.choicelists.ChoiceList>`
- :class:`Workflow <lino.core.workflows.Workflow>`

- :class:`Genders <lino.core.choicelists.Genders>`

- :class:`UserProfiles <lino.utils.auth.UserProfiles>`
- :class:`UserGroups <lino.utils.auth.UserGroups>`
- :class:`UserLevels <lino.utils.auth.UserLevels>`


"""

import logging
logger = logging.getLogger(__name__)


from lino.core.tables import VirtualTable

from north.dbutils import resolve_model, UnresolvedModel

from lino.core.modeltools import resolve_app, resolve_field, get_field
from django_site.modeltools import obj2str
from django_site.modeltools import obj2unicode
from django_site.modeltools import range_filter
from django_site.modeltools import full_model_name
from django_site.modeltools import models_by_base

from lino.core.model import Model
from lino.core.merge import MergeAction

#~ from lino.core.table import fields_list, inject_field
from lino.core.dbtables import has_fk
from lino.core.dbtables import Table
from django.db.models.fields import FieldDoesNotExist
from django.db import models
from django.conf import settings
#~ Model = models.Model
#~ from lino.core import table
#~ Table = table.Table

from lino.core.dbtables import summary, summary_row

from lino.core.frames import Frame
#~ from lino.core.dialogs import Dialog

from lino.core.actions import action
#~ from lino.core.actions import Action
from lino.core.actions import RowAction
AjaxAction = RowAction

from lino.mixins import AuthorRowAction
#~ from lino.core.actions import ListAction
from lino.core.actions import GridEdit, ShowDetailAction
from lino.core.actions import InsertRow, DeleteSelected
from lino.core.actions import SubmitDetail, SubmitInsert
#~ from lino.core.actions import Calendar

from lino.core.choicelists import ChoiceList, Choice
from lino.core.choicelists import Genders
from lino.core.workflows import Workflow, ChangeStateAction
#~ from lino.core.changes import ChangeStateAction
from lino.core.actions import NotifyingAction


from lino.core.fields import fields_list
from lino.core.fields import DummyField
from lino.core.fields import RecurrenceField
from lino.core.fields import GenericForeignKey
from lino.core.fields import GenericForeignKeyIdField
from lino.core.fields import IncompleteDateField
from lino.core.fields import DatePickerField
from lino.core.fields import NullCharField
from lino.core.fields import PasswordField
from lino.core.fields import MonthField
from lino.core.fields import PercentageField
#~ from lino.core.fields import LinkedForeignKey
from lino.core.fields import QuantityField
from lino.core.fields import HtmlBox, PriceField, RichTextField

from lino.core.fields import DisplayField, displayfield
from lino.core.fields import VirtualField, virtualfield
from lino.core.fields import RequestField, requestfield
from lino.core.fields import Constant, constant
from lino.core.fields import ForeignKey
from lino.core.fields import BabelTextField

from north.babel import BabelCharField, BabelNamed, LanguageField
#~ from north.babel import BabelCharField, BabelTextField, BabelNamed, LanguageField
#~ from lino.core.fields import MethodField

from lino.utils.choosers import chooser
from lino.utils.mti import EnableChild

from lino.utils.auth import UserLevels, UserProfiles, UserGroups

#~ from lino.base.utils import UserLevels, UserGroups, UserProfiles

from lino.core.layouts import FormLayout, Panel
from lino.core.layouts import ParamsLayout
#~ from lino.core.layouts import ActionParamsLayout
#~ DetailLayout = InsertLayout = FormLayout

#~ from lino.core.layouts import DetailLayout, InsertLayout


from lino.core.signals import pre_ui_create, pre_ui_delete, pre_ui_update, ChangeWatcher
from django_site.signals import startup

from lino.core.signals import pre_analyze
from lino.core.signals import post_analyze
from lino.core.signals import auto_create
from lino.core.signals import pre_merge
from lino.core.signals import pre_add_child
from lino.core.signals import pre_remove_child
from lino.core.signals import pre_ui_build
from lino.core.signals import post_ui_build

from django.db.models.signals import pre_save, post_save
from django.db.backends.signals import connection_created


from django.db.models.signals import class_prepared
from django.db.models.fields import NOT_PROVIDED


from django.dispatch import receiver
#~ from lino.core import signals


#~ class Module(object):
    #~ pass

from lino.core.inject import inject_field
from lino.core.inject import update_field
from lino.core.inject import inject_quick_add_buttons
from lino.core.inject import do_when_prepared, when_prepared
 
  
    
def add_user_group(name,label):
    """
    Add a user group to the :class:`UserGroups <lino.core.perms.UserGroups>` 
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
    
from lino.core.actors import get_default_required as required
    
class PseudoRequest:
    def __init__(self,username):
        self.username = username
        self._user = None
        
    def get_user(self):
        if self._user is None:
            if settings.SITE.user_model is not None:
                #~ print 20130222, self.username
                self._user = settings.SITE.user_model.objects.get(username=self.username)
        return self._user
    user = property(get_user)
    

