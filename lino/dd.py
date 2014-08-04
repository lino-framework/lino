# Copyright 2011-2014 Luc Saffre
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

"""See :doc:`/dev/dd`.

Tables:

- :class:`Table <lino.core.dbtables.Table>`
- :class:`VirtualTable <lino.core.tables.VirtualTable>`
- :class:`VentilatingTable <lino.core.tables.VentilatingTable>`
- :class:`EmptyTable <lino.mixins.EmptyTable>`
- :class:`Report <lino.mixins.Report>`
- :class:`Frame <lino.core.frames.Frame>`

Extended Fields:

- :class:`CharField <fields.CharField>`
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
- :class:`CustomField <lino.core.fields.CustomField>`
- :class:`RecurrenceField <lino.core.fields.RecurrenceField>`
- :class:`DummyField <lino.core.fields.DummyField>`
- :func:`ForeignKey <lino.core.fields.ForeignKey>`

Multilingual database content:

- :class:`BabelNamed <lino.mixins.BabelNamed>`
- :class:`BabelCharField <north.dbutils.BabelCharField>`
- :class:`BabelTextField <fields.BabelTextField>`
- :class:`LanguageField <north.dbutils.LanguageField>`
- :class:`babelkw <north.dbutils.babelkw>`
- :func:`babelattr <north.dbutils.babelattr>`
- :setting:`babelitem`
- :setting:`field2kw`

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

Parameter panels:

- :class:`dd.ObservedPeriod <lino.core.actors.ObservedPeriod>`
- :class:`dd.Yearly <lino.core.actors.Yearly>`
- :class:`dd.Today <lino.core.actors.Today>`

  
Utilities:

- :func:`obj2str <djangosite.dbutils.obj2str>`
- :func:`obj2unicode <djangosite.dbutils.obj2unicode>`
- :func:`range_filter <djangosite.dbutils.range_filter>`,
  :func:`inrange_filter <djangosite.dbutils.inrange_filter>`
- :func:`full_model_name <djangosite.dbutils.full_model_name>`
- :func:`fields_list <lino.core.fields.fields_list>`
- :func:`chooser <lino.utils.choosers.chooser>`

Inter-app relations:

- :func:`resolve_field <lino.core.dbutils.resolve_field>`
- :func:`resolve_model <north.dbutils.resolve_model>`
- :func:`resolve_app <lino.core.dbutils.resolve_app>`
- :func:`update_field <lino.core.inject.update_field>`
- :func:`inject_field <lino.core.inject.inject_field>`
- :func:`inject_action <lino.core.inject.inject_action>`
- :func:`update_model <lino.core.inject.update_model>`

- :func:`inject_quick_add_buttons <lino.core.inject.inject_quick_add_buttons>`
- :func:`models_by_base <djangosite.dbutils.models_by_base>`

Signals:

- See :ref:`lino.signals`

Actions:

- :class:`AuthorAction <lino.mixins.AuthorAction>`
- :class:`Action <lino.core.actions.Action>`
- :class:`ChangeStateAction <lino.core.workflows.ChangeStateAction>`
- :class:`NotifyingAction <lino.core.actions.NotifyingAction>`
- :class:`MergeAction <lino.core.merge.MergeAction>`
- :class:`ShowSlaveTable <lino.core.actions.ShowSlaveTable>`
- :class:`PrintTableAction <lino.utils.appy_pod.PrintTableAction>`
- :class:`PrintLabelsAction <lino.utils.appy_pod.PrintLabelsAction>`

Permissions:

- :class:`UserProfiles <lino.core.auth.UserProfiles>`
- :class:`UserGroups <lino.core.auth.UserGroups>`
- :class:`UserLevels <lino.core.auth.UserLevels>`
- :func:`add_user_group <lino.core.auth.add_user_group>` 


Workflows:

- :class:`ChoiceList <lino.core.choicelists.ChoiceList>`
- :class:`Workflow <lino.core.workflows.Workflow>`
- :class:`State <lino.core.workflows.State>`

Model mixins:

- :class:`lino.mixins.ProjectRelated`
- :class:`lino.mixins.UserAuthored`
- :class:`lino.mixins.ByUser`
- :class:`Sequenced <lino.mixins.Sequenced>`
- :class:`Duplicable <lino.mixins.duplicable.Duplicable>`
- :class:`lino.mixins.Referrable`
- :class:`lino.mixins.Registrable`
- :class:`lino.mixins.Hierarizable`

- :class:`Created <lino.mixins.Created>` and :class:`Modified
  <lino.mixins.Modified>` (and their deprecated combination
  :class:`CreatedModified <lino.mixins.CreatedModified>`)

- :class:`lino.mixins.printable.Printable`
- :class:`lino.mixins.printable.PrintableType`
- :class:`lino.mixins.printable.TypedPrintable`
- :class:`lino.mixins.printable.CachedPrintable`
- :class:`lino.mixins.uploadable.Uploadable`
- :class:`lino.mixins.human.Human`
- :class:`lino.mixins.human.Born`
- :class:`Addressable <lino.mixins.addressable.Addressable>`

Miscellaneous:

- :class:`Genders <lino.core.choicelists.Genders>`

"""

from __future__ import unicode_literals
from __future__ import print_function


import logging
logger = logging.getLogger(__name__)

# logger.info("20140227 dd.py a")

# from djangosite import Plugin
# from lino.ad import Plugin

from lino.core.tables import VirtualTable
from lino.mixins import EmptyTable
from lino.mixins import Report


from north.dbutils import resolve_model, UnresolvedModel

from lino.core.dbutils import resolve_app, require_app_models
from lino.core.dbutils import resolve_field, get_field
from djangosite.dbutils import obj2str
from djangosite.dbutils import obj2unicode
from djangosite.dbutils import range_filter
from djangosite.dbutils import inrange_filter
from djangosite.dbutils import full_model_name
from djangosite.dbutils import models_by_base

from lino.core.model import Model
from lino.core.merge import MergeAction

#~ from lino.core.table import fields_list, inject_field
from lino.core.actors import (ParameterPanel, ObservedPeriod)
from lino.core.actors import Today
from lino.core.actors import Yearly
from lino.core.dbtables import has_fk
from lino.core.dbtables import Table
from django.db.models.fields import FieldDoesNotExist
from django.db import models
from django.conf import settings
#~ Model = models.Model
#~ from lino.core import table
#~ Table = table.Table

#~ from lino.core.dbtables import summary, summary_row

from lino.core.frames import Frame
from lino.core.tables import VentilatingTable
#~ from lino.core.dialogs import Dialog

from lino.core.actions import action
#~ from lino.core.actions import Action
from lino.core.actions import Action
from lino.core.actions import MultipleRowAction
#~ RowAction = CustomAction
#~ Action = CustomAction
from lino.core.actions import ShowSlaveTable

from lino.mixins import AuthorAction
#~ from lino.core.actions import ListAction
from lino.core.actions import GridEdit, ShowDetailAction
from lino.core.actions import InsertRow, DeleteSelected
from lino.core.actions import SubmitDetail, SubmitInsert
#~ from lino.core.actions import Calendar

from lino.core.choicelists import ChoiceList, Choice
from lino.core.choicelists import Genders
from lino.core.choicelists import YesNo
from lino.core.workflows import State, Workflow, ChangeStateAction
from lino.core.actions import NotifyingAction


from lino.core.fields import fields_list, ImportedFields
from lino.core.fields import Dummy, DummyField

# 20140314 need a Dummy object to define a dummy module
# from lino.core.layouts import BaseLayout as Dummy  # 20140314
# from lino.core.actors import Actor as Dummy  # 20140314

from lino.core.fields import CustomField
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
from lino.core.fields import CharField

from lino.mixins import BabelNamed
from lino.utils.appy_pod import PrintTableAction
from lino.utils.appy_pod import PrintLabelsAction

from lino.mixins.addressable import Addressable

from north.dbutils import BabelCharField, LanguageField

from north.dbutils import babelkw
from north.dbutils import babelattr
from north.dbutils import babel_values  # alias for babelkw for backward compat

from lino.utils.choosers import chooser, action_chooser
from lino.utils.mti import EnableChild

#~ from lino.core.auth import UserLevels, UserProfiles, UserGroups, add_user_group
from lino.core.perms import UserLevels, UserProfiles, UserGroups, add_user_group

#~ from lino.base.utils import UserLevels, UserGroups, UserProfiles

from lino.core.layouts import FormLayout, Panel
from lino.core.layouts import ParamsLayout
#~ from lino.core.layouts import ActionParamsLayout
#~ DetailLayout = InsertLayout = FormLayout

#~ from lino.core.layouts import DetailLayout, InsertLayout


from lino.core.signals import pre_ui_create, pre_ui_delete, pre_ui_update, ChangeWatcher
from lino.core.signals import database_connected
#~ from lino.core.signals import database_ready
from djangosite.signals import database_ready

from djangosite.signals import pre_startup, post_startup

from lino.core.signals import pre_analyze
from lino.core.signals import post_analyze
from lino.core.signals import auto_create
from lino.core.signals import pre_merge
from lino.core.signals import pre_add_child
from lino.core.signals import pre_remove_child
from lino.core.signals import pre_ui_build
from lino.core.signals import post_ui_build

from django.db.models.signals import pre_save, post_save
from django.db.models.signals import pre_init, post_init
from django.db.models.signals import class_prepared

from django.db.backends.signals import connection_created

from django.dispatch import receiver
#~ from lino.core import signals


from django.db.models.fields import NOT_PROVIDED

#~ class Module(object):
    #~ pass

from lino.core.inject import inject_action
from lino.core.inject import inject_field
from lino.core.inject import update_model
from lino.core.inject import update_field
from lino.core.inject import inject_quick_add_buttons
from lino.core.inject import do_when_prepared, when_prepared


from lino.core.actors import get_default_required as required
Required = required


class PseudoRequest:

    def __init__(self, username):
        self.username = username
        self._user = None

    def get_user(self):
        if self._user is None:
            if settings.SITE.user_model is not None:
                #~ print 20130222, self.username
                self._user = settings.SITE.user_model.objects.get(
                    username=self.username)
        return self._user
    user = property(get_user)


from lino.utils import IncompleteDate

from north.dbutils import fds, fdm, fdl, fdf, fdmy
from north.dbutils import fds as fds_


def fds(d):
    """
    Adds support for :class:`lino.fields.IncompleteDate`.
    """
    if isinstance(d, IncompleteDate):
        return fds_(d.as_date())
    return fds_(d)

# backward compatibility
dtos = fds
from north.dbutils import fdl as dtosl
#~ from north.dbutils import dtos as dtos_

babelitem = settings.SITE.babelitem
field2kw = settings.SITE.field2kw

from lino.mixins import (
    ProjectRelated, UserAuthored, ByUser,
    Duplicable, Duplicate,
    Sequenced, Hierarizable, Referrable,
    Registrable,
    Controllable)

from lino.mixins import Created, Modified
from lino.mixins import CreatedModified  # deprecated

from lino.mixins.printable import Printable, PrintableType, CachedPrintable, TypedPrintable, DirectPrintAction
#~ from lino.mixins import SimplyPrintable
from lino.mixins.uploadable import Uploadable
from lino.mixins.human import Human, Born

from lino.mixins.periods import DatePeriod, PeriodEvents

#~ from lino.utils.screenshots import register_screenshot

from django.utils.importlib import import_module

from django.contrib.contenttypes.models import ContentType


# The following are not only shortcuts, they also are a preparation to
# encapsulate the `settings.SITE` name. It is possible that after
# Django 1.7 we no longer need a `settings.SITE`. So I plan to
# deprecate direct access to settings.SITE in application code. I am
# not yet 100% sure whether this is possible and makes sense.

# site = settings.SITE
plugins = apps = settings.SITE.plugins
modules = settings.SITE.modules
login = settings.SITE.login
startup = settings.SITE.startup
get_db_overview_rst = settings.SITE.get_db_overview_rst
is_abstract_model = settings.SITE.is_abstract_model
is_installed = settings.SITE.is_installed
str2kw = settings.SITE.str2kw
today = settings.SITE.today


def resolve_plugin(app_label):
    return plugins.get(app_label, None)


def show(*args, **kw):
    return login().show(*args, **kw)

from django.utils import translation
get_language = translation.get_language

# logger.info("20140227 dd.py b %s", site)
