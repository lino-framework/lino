# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :mod:`lino.api.dd` module is a shortcut to those parts of Lino which
are used in your :xfile:`models.py` modules.  The name ``dd`` stands
for "Database Design".

Application:

- :attr:`plugins <lino.core.site.Site.plugins>`
- :attr:`decfmt <lino.core.site.Site.decfmt>`
- :attr:`str2kw <lino.core.site.Site.str2kw>`
- :attr:`today <lino.core.site.Site.today>`
- :attr:`strftime <lino.core.site.Site.strftime>`
- :attr:`demo_date <lino.core.site.Site.demo_date>`
- :attr:`is_abstract_model <lino.core.site.Site.is_abstract_model>`
- :attr:`is_installed <lino.core.site.Site.is_installed>`
- :attr:`add_welcome_handler <lino.core.site.Site.add_welcome_handler>`
- :attr:`build_media_url <lino.core.site.Site.build_media_url>`
- :attr:`get_default_language <lino.core.site.Site.get_default_language>`


Tables:

- :class:`Table <lino.core.dbtables.Table>`
- :class:`VirtualTable`
- :class:`VentilatingTable`
- :class:`Frame <lino.core.frames.Frame>`
- :class:`ChoiceList <lino.core.choicelists.ChoiceList>`

Extended Fields:

- :class:`CharField <fields.CharField>`
- :class:`NullCharField <lino.core.fields.NullCharField>`
- :class:`IncompleteDateField <lino.core.fields.IncompleteDateField>`
- :class:`PasswordField <lino.core.fields.PasswordField>`
- :class:`MonthField <lino.core.fields.MonthField>`
- :class:`PercentageField <lino.core.fields.PercentageField>`
- :class:`QuantityField <lino.core.fields.QuantityField>`
- :class:`PriceField<lino.core.fields.PriceField>`
- :class:`CustomField <lino.core.fields.CustomField>`
- :class:`RecurrenceField <lino.core.fields.RecurrenceField>`
- :class:`DummyField <lino.core.fields.DummyField>`
- :func:`ForeignKey <lino.core.fields.ForeignKey>`

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

- :func:`obj2str <lino.core.utils.obj2str>`
- :func:`obj2unicode <lino.core.utils.obj2unicode>`
- :func:`range_filter <lino.core.utils.range_filter>`,
  :func:`inrange_filter <lino.core.utils.inrange_filter>`
- :func:`full_model_name <lino.core.utils.full_model_name>`
- :func:`fields_list <lino.core.fields.fields_list>`
- :func:`chooser <lino.utils.choosers.chooser>`
- :class: `ParameterPanel <lino.core.utils.ParameterPanel>`


Inter-app relations:

- :func:`resolve_field <lino.core.utils.resolve_field>`
- :func:`resolve_model <lino.core.utils.resolve_model>`
- :func:`resolve_app <lino.core.utils.resolve_app>`
- :func:`update_field <lino.core.inject.update_field>`
- :func:`inject_field <lino.core.inject.inject_field>`
- :func:`inject_action <lino.core.inject.inject_action>`
- :func:`update_model <lino.core.inject.update_model>`

- :func:`inject_quick_add_buttons <lino.core.inject.inject_quick_add_buttons>`

Signals:

- See :ref:`lino.signals`

Actions:

- :class:`Action <lino.core.actions.Action>`
- :class:`ChangeStateAction <lino.core.workflows.ChangeStateAction>`
- :class:`NotifyingAction <lino.core.actions.NotifyingAction>`
- :class:`MergeAction <lino.core.merge.MergeAction>`
- :class:`ShowSlaveTable <lino.core.actions.ShowSlaveTable>`
- :class:`PrintTableAction <lino.utils.appy_pod.PrintTableAction>`

Permissions:

- :class:`UserGroups <lino.modlib.users.mixins.UserGroups>`
- :class:`UserLevels <lino.modlib.users.mixins.UserLevels>`
- :func:`add_user_group <lino.modlib.users.mixins.add_user_group>`


Workflows:

- :class:`Workflow <lino.core.workflows.Workflow>`
- :class:`State <lino.core.workflows.State>`


"""

from __future__ import unicode_literals
from __future__ import print_function


import logging
logger = logging.getLogger(__name__)
"""
Shortcut to the main Lino logger.
"""

# logger.info("20140227 dd.py a")

from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from lino.core.tables import VirtualTable

from lino.core.utils import resolve_model, UnresolvedModel

from lino.core.utils import resolve_app, require_app_models
from lino.core.utils import resolve_field, get_field
from lino.core.utils import obj2str
from lino.core.utils import obj2unicode
from lino.core.utils import range_filter
from lino.core.utils import inrange_filter
from lino.core.utils import full_model_name

from lino.core.model import Model
"Shortcut to :class:`lino.core.model.Model`."

from lino.core.merge import MergeAction

from lino.core.actors import Actor

from lino.core.dbtables import has_fk
from lino.core.dbtables import Table
from django.db.models.fields import FieldDoesNotExist
from django.db import models

from lino.core.frames import Frame
from lino.core.tables import VentilatingTable

from lino.core.actions import action
from lino.core.actions import Action
from lino.core.actions import MultipleRowAction
from lino.core.actions import ShowSlaveTable

from lino.core.actions import GridEdit, ShowDetailAction
from lino.core.actions import InsertRow, DeleteSelected
from lino.core.actions import SubmitDetail, SubmitInsert

from lino.core.choicelists import ChoiceList, Choice
from lino.core.workflows import State, Workflow, ChangeStateAction
from lino.core.actions import NotifyingAction


from lino.core.fields import fields_list, ImportedFields
from lino.core.fields import Dummy, DummyField

# 20140314 need a Dummy object to define a dummy module
# from lino.core.layouts import BaseLayout as Dummy  # 20140314
# from lino.core.actors import Actor as Dummy  # 20140314

from lino.core.fields import CustomField
from lino.core.fields import RecurrenceField
from lino.core.fields import IncompleteDateField
from lino.core.fields import DatePickerField
from lino.core.fields import NullCharField
from lino.core.fields import PasswordField
from lino.core.fields import MonthField
from lino.core.fields import PercentageField
#~ from lino.core.fields import LinkedForeignKey
from lino.core.fields import QuantityField
from lino.core.fields import DurationField
from lino.core.fields import HtmlBox, PriceField, RichTextField

from lino.core.fields import DisplayField, displayfield, htmlbox
from lino.core.fields import VirtualField, virtualfield
from lino.core.fields import RequestField, requestfield
from lino.core.fields import Constant, constant
from lino.core.fields import ForeignKey
from lino.core.fields import CharField

# from lino_xl.lib.appypod.mixins import PrintTableAction

from lino.core.utils import babelkw
# from lino.core.utils import babelattr
from lino.core.utils import babel_values  # alias for babelkw for backward compat

from lino.utils.choosers import chooser, action_chooser

from lino.core.layouts import FormLayout, DetailLayout, InsertLayout, Panel
from lino.core.layouts import ParamsLayout
from lino.core.layouts import DummyPanel


from lino.core.signals import on_ui_created, pre_ui_delete, on_ui_updated

from lino.core.signals import database_connected
from lino.core.signals import database_ready
from lino.core.signals import pre_startup, post_startup
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

from lino.core.utils import ParameterPanel, PseudoRequest

#from lino.modlib.users.choicelists import UserLevels, UserGroups
#from lino.modlib.users.utils import add_user_group


from lino.utils import IncompleteDate

from lino.utils.format_date import fdm, fdl, fdf, fdmy
from lino.utils.format_date import fds as fds_


def fds(d):
    """
    Adds support for :class:`lino.fields.IncompleteDate`.
    """
    if isinstance(d, IncompleteDate):
        return fds_(d.as_date())
    return fds_(d)

# backward compatibility
dtos = fds
from lino.utils.format_date import fdl as dtosl

babelitem = settings.SITE.babelitem
field2kw = settings.SITE.field2kw

from lino.utils.mldbc.fields import BabelTextField
from lino.utils.mldbc.fields import BabelCharField, LanguageField

from lino.modlib.system.choicelists import Genders, PeriodEvents, YesNo

from importlib import import_module

# The following are not only shortcuts, they also are a preparation to
# encapsulate the `settings.SITE` name. It is possible that after
# Django 1.7 we no longer need a `settings.SITE`. So I plan to
# deprecate direct access to settings.SITE in application code. I am
# not yet 100% sure whether this will be possible and makes sense.

decfmt = settings.SITE.decfmt
str2kw = settings.SITE.str2kw


def today(*args, **kwargs):
    # make it serializable for Django migrations
    return settings.SITE.today(*args, **kwargs)
# today = settings.SITE.today
strftime = settings.SITE.strftime
demo_date = settings.SITE.demo_date
is_abstract_model = settings.SITE.is_abstract_model
is_installed = settings.SITE.is_installed
# get_db_overview_rst = settings.SITE.get_db_overview_rst
add_welcome_handler = settings.SITE.add_welcome_handler
build_media_url = settings.SITE.build_media_url
build_static_url = settings.SITE.build_static_url
get_default_language = settings.SITE.get_default_language
get_language_info = settings.SITE.get_language_info
resolve_languages = settings.SITE.resolve_languages
babelattr = settings.SITE.babelattr

apps = plugins = settings.SITE.plugins
# `apps` is an alias for `plugins`. We recommend plugins since `apps`
# is being used by Django 1.7


def resolve_plugin(app_label):
    return plugins.get(app_label, None)

from django.utils import translation
get_language = translation.get_language

from lino.core.roles import SiteStaff, SiteUser, SiteAdmin, login_required


# deprecated aliases:
Required = required = login_required

# logger.info("20140227 dd.py b %s", site)

