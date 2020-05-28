# -*- coding: UTF-8 -*-
# Copyright 2011-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


import logging ; logger = logging.getLogger(__name__)

# logger.info("20140227 dd.py a")

from django.conf import settings
from django.db.models import *

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

from lino.core.actions import ShowTable, ShowDetail
from lino.core.actions import ShowInsert, DeleteSelected
from lino.core.actions import SubmitDetail, SubmitInsert

from lino.core.choicelists import ChoiceList, Choice
from lino.core.workflows import State, Workflow, ChangeStateAction


from lino.core.fields import fields_list, ImportedFields
from lino.core.fields import Dummy, DummyField
from lino.core.fields import TimeField

# 20140314 need a Dummy object to define a dummy module
# from lino.core.layouts import BaseLayout as Dummy  # 20140314
# from lino.core.actors import Actor as Dummy  # 20140314

from lino.core.fields import CustomField
from lino.core.fields import RecurrenceField
from lino.core.fields import IncompleteDateField
from lino.core.fields import DatePickerField
# from lino.core.fields import NullCharField
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
from lino.core.fields import ForeignKey, OneToOneField
from lino.core.fields import CharField

# from lino_xl.lib.appypod.mixins import PrintTableAction

from lino.core.utils import babelkw
# from lino.core.utils import babelattr
from lino.core.utils import babel_values  # alias for babelkw for backward compat

from lino.utils.choosers import chooser, action_chooser

# from lino.core.layouts import FormLayout
from lino.core.layouts import DetailLayout, InsertLayout, Panel
from lino.core.layouts import ParamsLayout, ActionParamsLayout
from lino.core.layouts import DummyPanel


from lino.core.signals import on_ui_created, pre_ui_delete, on_ui_updated

# from lino.core.signals import database_connected
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

from lino.core.inject import inject_action
from lino.core.inject import inject_field
from lino.core.inject import update_model
from lino.core.inject import update_field
from lino.core.inject import inject_quick_add_buttons
from lino.core.inject import do_when_prepared, when_prepared

from lino.core.utils import ParameterPanel, PseudoRequest

from lino.utils import IncompleteDate

from lino.utils.format_date import fdm, fdl, fdf, fdmy
from lino.utils.format_date import fds as fds_


def fds(d):
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

# apps = plugins = settings.SITE.plugins
plugins = settings.SITE.plugins
# `apps` is a deprecated alias for `plugins`. We recommend plugins
# since `apps` is being used by Django 1.7

format_currency = settings.SITE.format_currency


def resolve_plugin(app_label):
    return plugins.get(app_label, None)

from django.utils import translation
get_language = translation.get_language

from lino.core.roles import SiteStaff, SiteUser, SiteAdmin, login_required

# logger.info("20140227 dd.py b %s", site)

try:
    import schedule
except ImportError as e:
    # logger.info("schedule not installed (%s)", e)
    schedule = None


def schedule_often(every=10):
    def decorator(func):
        if settings.SITE.use_linod:
            schedule.every(every).seconds.do(func)
        return func
    return decorator


def schedule_daily(at="20:00"):
    def decorator(func):
        if settings.SITE.use_linod:
            # schedule.every(10).seconds.do(func)
            schedule.every().day.at(at).do(func)
        return func
    return decorator
