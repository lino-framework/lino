# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.changes`.

It defines the :class:`Change` model, and the functions
:func:`watch_changes` and :func:`watch_all_changes`.  It also adds a
menu entry to the `Explorer` menu.

See also :ref:`lino.tutorial.watch`.

"""
from past.builtins import basestring
from builtins import object

import logging

logger = logging.getLogger(__name__)

import datetime

from django.conf import settings

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from lino.api import dd
from lino.core import fields

from lino.core.roles import SiteStaff
from lino.core.signals import pre_ui_delete, on_ui_created, on_ui_updated
from lino.core.signals import pre_merge
from lino.core.signals import pre_add_child, pre_remove_child
from lino.core.signals import receiver

from lino.modlib.gfks.fields import GenericForeignKey, GenericForeignKeyIdField


class ChangeTypes(dd.ChoiceList):
    """
    The list of possible choices for the `type` field
    of a :class:`Change`.
    """
    # app_label = 'lino'
    verbose_name = _("Change Type")
    verbose_name_plural = _("Change Types")


add = ChangeTypes.add_item
add('C', _("Create"), 'create')
add('U', _("Update"), 'update')
add('D', _("Delete"), 'delete')
add('R', _("Remove child"), 'remove_child')
add('A', _("Add child"), 'add_child')
add('M', _("Merge"), 'merge')


@dd.python_2_unicode_compatible
class Change(dd.Model):
    """A registered change in the database.

    Each database change of a watched object will generate one Change
    record.

    .. attribute:: master

        The database object which acts as "master".
    
    .. attribute:: object

        The database object which has been modified.
    
    
    """

    class Meta(object):
        verbose_name = _("Change")
        verbose_name_plural = _("Changes")

    # allow_cascaded_delete = 'master'

    time = models.DateTimeField()
    type = ChangeTypes.field()
    if settings.SITE.user_model:
        user = dd.ForeignKey(settings.SITE.user_model)
    else:
        user = dd.DummyField()

    object_type = models.ForeignKey(
        'contenttypes.ContentType', blank=True, null=True,
        verbose_name=_("Object type"),
        related_name='changes_by_object')
    object_id = GenericForeignKeyIdField(
        object_type, blank=True, null=True)
    object = GenericForeignKey('object_type', 'object_id', _("Object"))

    master_type = models.ForeignKey(
        'contenttypes.ContentType', blank=True, null=True,
        verbose_name=_("Master type"), related_name='changes_by_master')
    master_id = GenericForeignKeyIdField(
        master_type, blank=True, null=True)
    master = GenericForeignKey('master_type', 'master_id', _("Master"))

    diff = dd.RichTextField(_("Changes"), format='plain', blank=True)

    def __str__(self):
        # ~ return "#%s - %s" % (self.id,self.time)
        return "#%s" % self.id


class Changes(dd.Table):
    """The default table for :class:`Change`.
    """

    param_object_type = models.ForeignKey(
        'contenttypes.ContentType',
        verbose_name=_("Object type"), blank=True)
    parameters = {
        'change_type': ChangeTypes.field(force_selection=False, blank=True),
        'date': models.DateField(_("Only changes from"), blank=True),
        'object_type': param_object_type,
        'object_id': models.PositiveIntegerField("Object ID", blank=True),
    }
    if settings.SITE.user_model:
        parameters['user'] = dd.ForeignKey(
            settings.SITE.user_model,
            blank=True)

    required_roles = dd.required(SiteStaff)

    editable = False
    model = 'changes.Change'
    order_by = ['-time']

    detail_layout = """
        time user type master object id
        diff
    """

    params_layout = """
        date user change_type object_type object_id
    """

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Changes, cls).get_request_queryset(ar)
        if not isinstance(qs, list):
            if ar.param_values.change_type:
                qs = qs.filter(type=ar.param_values.change_type)
            if ar.param_values.date:
                qs = qs.filter(time__range=(
                    ar.param_values.date,
                    ar.param_values.date+datetime.timedelta(1)))
            if settings.SITE.user_model and ar.param_values.user:
                qs = qs.filter(user=ar.param_values.user)
            if ar.param_values.object_type:
                qs = qs.filter(object_type=ar.param_values.object_type)
            if ar.param_values.object_id:
                qs = qs.filter(object_id=ar.param_values.object_id)
        return qs


class ChangesByObject(Changes):
    """Slave Table showing the direct changes related to the current
    object.

    """
    required_roles = dd.required(SiteStaff)
    master_key = 'object'
    column_names = 'time user type master diff master_type master_id'


class ChangesByMaster(Changes):
    """Slave Table showing the changes related to the current object,
    including those applied to "child" objects.

    """
    required_roles = dd.required()
    master_key = 'master'
    # column_names = 'time user type object diff object_type object_id'
    column_names = 'time user type object diff *'


class WatcherSpec(object):
    def __init__(self, ignored_fields, get_master):
        self.ignored_fields = ignored_fields
        self.get_master = get_master


def watch_all_changes(ignore=[]):

    """Call this to activate change watching on *all* models. The default
    behaviour is to watch only models that have been explicitly
    declared using :func:`watch_changes`.

    This is a fallback method and settings passed to specific model
    using `watch_changes` call takes precedence.


    :param ignore: specify list of model names to ignore

    """
    watch_all_changes.allow = True
    watch_all_changes.ignore.extend(ignore)

watch_all_changes.allow = False
watch_all_changes.ignore = []


def return_self(obj):
    return obj


def watch_changes(model, ignore=[], master_key=None, **options):
    """Declare the specified model to be "observed" ("watched") for changes.
    Each change to an object comprising at least one watched field
    will lead to an entry to the `Changes` table.

    `ignore` should be a string with a space-separated list of field
    names to be ignored.
    
    All calls to watch_changes will be grouped by model.

    """
    if isinstance(ignore, basestring):
        ignore = fields.fields_list(model, ignore)
    if isinstance(master_key, basestring):
        fld = model.get_data_elem(master_key)
        if fld is None:
            raise Exception("No field %r in %s" % (master_key, model))
        master_key = fld
    if isinstance(master_key, fields.RemoteField):
        get_master = master_key.func
    elif master_key is None:
        get_master = return_self
    else:
        def get_master(obj):
            return getattr(obj, master_key.name)
    ignore = set(ignore)
    cs = model.change_watcher_spec
    if cs is not None:
        ignore |= cs.ignored_fields
    for f in model._meta.fields:
        if not f.editable:
            ignore.add(f.name)
    model.change_watcher_spec = WatcherSpec(ignore, get_master)


def get_change_watcher_spec(obj):
    cs = obj.change_watcher_spec

    if cs is None:
        if not watch_all_changes.allow \
           or obj.__class__.__name__ in watch_all_changes.ignore:
            return None

        cs = WatcherSpec([], return_self)
        obj.change_watcher_spec = cs

    return cs


def get_master(obj):
    cs = get_change_watcher_spec(obj)

    if cs:
        return cs.get_master(obj)


def log_change(type, request, master, obj, msg=''):
    Change(
        type=type,
        time=timezone.now(),
        user=request.user,
        master=master,
        object=obj,
        diff=msg).save()


@receiver(on_ui_updated)
def on_update(sender=None, watcher=None, request=None, **kw):
    """
    Log a Change if there is a `change_watcher_spec`.
    """
    master = get_master(watcher.watched)
    if master is None:
        # No master, nothing to log
        return

    cs = watcher.watched.change_watcher_spec
    changes = []
    for k, old, new in watcher.get_updates(cs.ignored_fields):
        changes.append("%s : %s --> %s" %
                       (k, dd.obj2str(old), dd.obj2str(new)))
    if len(changes) == 0:
        msg = '(no changes)'
    elif len(changes) == 1:
        msg = changes[0]
    else:
        msg = '- ' + ('\n- '.join(changes))
    log_change(ChangeTypes.update, request, master, watcher.watched, msg)


@receiver(pre_ui_delete)
def on_delete(sender=None, request=None, **kw):
    """Calls :func:`log_change` with `ChangeTypes.delete`.

    Note that you must call this before actually deleting the object,
    otherwise mysql (not sqlite) says ERROR: (1048, "Column
    'object_id' cannot be null")

    """
    master = get_master(sender)
    if master is None:
        return
    log_change(ChangeTypes.delete, request, master,
               sender, dd.obj2str(sender, True))


@receiver(on_ui_created)
def on_create(sender=None, request=None, **kw):
    """To be called when a new instance has actually been created and
    saved.

    """
    master = get_master(sender)
    if master is None:
        return
    log_change(ChangeTypes.create, request, master,
               sender, dd.obj2str(sender, True))


@receiver(pre_add_child)
def on_add_child(sender=None, request=None, child=None, **kw):
    master = get_master(sender)
    if master is None:
        return
    log_change(ChangeTypes.add_child, request, master,
               sender, dd.full_model_name(child))


@receiver(pre_remove_child)
def on_remove_child(sender=None, request=None, child=None, **kw):
    master = get_master(sender)
    if master is None:
        return
    log_change(ChangeTypes.remove_child, request,
               master, sender, dd.full_model_name(child))


@receiver(pre_merge)
def on_merge(sender=None, request=None, **kw):
    """
    """
    master = get_master(sender.obj)
    if master is None:
        return
    log_change(ChangeTypes.merge, request,
               master, sender.obj, sender.logmsg())

