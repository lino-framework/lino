# Copyright 2012-2013 Luc Saffre
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

"""
The :xfile:`models` module for :mod:`lino.modlib.changes`.

It defines the :class:`Change` model
and the :func:`watch_changes` function.
It also adds a menu entry to the `Explorer` menu.
"""

import logging

logger = logging.getLogger(__name__)

import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd
from lino.core import fields
from lino.utils.choosers import chooser

from lino.core.signals import pre_ui_delete, pre_ui_create, pre_ui_update
from lino.core.signals import pre_merge
from lino.core.signals import pre_add_child, pre_remove_child
from lino.core.signals import receiver


class ChangeTypes(dd.ChoiceList):
    """
    The list of possible choices for the `type` field
    of a :class:`Change`.
    """
    app_label = 'lino'
    verbose_name = _("Change Type")
    verbose_name_plural = _("Change Types")


add = ChangeTypes.add_item
add('C', _("Create"), 'create')
add('U', _("Update"), 'update')
add('D', _("Delete"), 'delete')
add('R', _("Remove child"), 'remove_child')
add('A', _("Add child"), 'add_child')
add('M', _("Merge"), 'merge')


class Change(dd.Model):
    """
    Each database change of a watched object will generate one Change record.
    """

    class Meta:
        verbose_name = _("Change")
        verbose_name_plural = _("Changes")

    time = models.DateTimeField()
    type = ChangeTypes.field()
    if settings.SITE.user_model:
        user = dd.ForeignKey(settings.SITE.user_model)

    object_type = models.ForeignKey(ContentType,
                                    related_name='changes_by_object',
                                    verbose_name=_("Object type"))
    object_id = dd.GenericForeignKeyIdField(object_type)
    object = dd.GenericForeignKey('object_type', 'object_id', _("Object"))
    # see blog/2013/0123

    master_type = models.ForeignKey(ContentType,
                                    related_name='changes_by_master',
                                    verbose_name=_("Master type"))
    master_id = dd.GenericForeignKeyIdField(master_type)
    master = dd.GenericForeignKey('master_type', 'master_id', _("Master"))

    diff = dd.RichTextField(_("Changes"), format='plain', blank=True)

    def __unicode__(self):
        # ~ return "#%s - %s" % (self.id,self.time)
        return "#%s" % self.id

    # NOTE: the following code is the same as in lino.mixins.Controllable
    # TODO: automate this behaviour in dd.GenericForeignKey
    @chooser(instance_values=True)
    def object_id_choices(cls, object_type):
        if object_type:
            return object_type.model_class().objects.all()
        return []

    def get_object_id_display(self, value):
        if self.object_type:
            try:
                return unicode(self.object_type.get_object_for_this_type(pk=value))
            except self.object_type.model_class().DoesNotExist, e:
                return "%s with pk %r does not exist" % (
                    dd.full_model_name(self.object_type.model_class()), value)

    @chooser(instance_values=True)
    def master_id_choices(cls, master_type):
        if master_type:
            return master_type.model_class().objects.all()
        return []

    def get_master_id_display(self, value):
        if self.master_type:
            try:
                return unicode(self.master_type.get_object_for_this_type(pk=value))
            except self.master_type.model_class().DoesNotExist, e:
                return "%s with pk %r does not exist" % (
                    dd.full_model_name(self.master_type.model_class()), value)
                # NOTE: the above code is the same as in lino.mixins.Controllable


class Changes(dd.Table):
    parameters = {
        'type': ChangeTypes.field(force_selection=False, blank=True),
        'date': models.DateField(_("Only changes from"), blank=True),
    }
    if settings.SITE.user_model:
        parameters['user'] = dd.ForeignKey(settings.SITE.user_model, blank=True)

    required = dd.required(user_level='admin')

    editable = False
    model = Change
    order_by = ['-time']
    detail_layout = """
    time user type master object id
    diff
    """

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Changes, cls).get_request_queryset(ar)
        if not isinstance(qs, list):
            if ar.param_values.type:
                qs = qs.filter(type=ar.param_values.type)
            if ar.param_values.date:
                qs = qs.filter(time__range=(ar.param_values.date, ar.param_values.date+datetime.timedelta(1)))
            if settings.SITE.user_model and ar.param_values.user:
                qs = qs.filter(user=ar.param_values.user)
        return qs


class ChangesByMaster(Changes):
    """
    Slave Table showing the changes related to the current object
    """
    required = dd.required()
    column_names = 'time user type object diff object_type object_id'
    master_key = 'master'


class WatcherSpec:
    def __init__(self, ignored_fields, get_master):
        self.ignored_fields = ignored_fields
        self.get_master = get_master


def watch_all_changes(ignore=[]):
    """
    Call to watch all changes on all models. This is fallback method and
    settings passed to specific model using `watch_changes` call takes precedence.


    :param ignore: specify list of model names to ignore
    """
    watch_all_changes.allow = True
    watch_all_changes.ignore.extend(ignore)

watch_all_changes.allow = False
watch_all_changes.ignore = []


def return_self(obj):
    return obj


def watch_changes(model, ignore=[], master_key=None, **options):
    """
    Declare the specified model to be "observed" ("watched") for changes.
    Each change to an object comprising at least one watched field
    will lead to an entry to the `Changes` table.
    
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
        if not watch_all_changes.allow or obj.__class__.__name__ in watch_all_changes.ignore:
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
        time=datetime.datetime.now(),
        user=request.user,
        master=master,
        object=obj,
        diff=msg).save()


@receiver(pre_ui_update)
def on_update(sender=None, request=None, **kw):
    # Note that sender is a Watcher instance
    master = get_master(sender.watched)
    if master is None:
        # No master, nothing to log
        return

    cs = sender.watched.change_watcher_spec
    changes = []
    for k, old in sender.original_state.iteritems():
        if not k in cs.ignored_fields:
            new = sender.watched.__dict__.get(k, dd.NOT_PROVIDED)
            if old != new:
                changes.append("%s : %s --> %s" %
                               (k, dd.obj2str(old), dd.obj2str(new)))
    if len(changes) == 0:
        msg = '(no changes)'
    elif len(changes) == 1:
        msg = changes[0]
    else:
        msg = '- ' + ('\n- '.join(changes))
    log_change(ChangeTypes.update, request, master, sender.watched, msg)


@receiver(pre_ui_delete)
def on_delete(sender=None, request=None, **kw):
    """
    Calls :func:`log_change` with `ChangeTypes.delete`.
    
    Note that you must call this before actually deleting the object,
    otherwise mysql (not sqlite) says 
    ERROR: (1048, "Column 'object_id' cannot be null")
    """
    master = get_master(sender)
    if master is None:
        return
    log_change(ChangeTypes.delete, request, master,
               sender, dd.obj2str(sender, True))


@receiver(pre_ui_create)
def on_create(sender=None, request=None, **kw):
    """
    To be called when a new instance has actually been created and saved.
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
    log_change(ChangeTypes.merge, request, master, sender.obj, sender.logmsg())


from lino.modlib.system.models import SYSTEM_USER_LABEL


def setup_explorer_menu(site, ui, profile, m):
    system = m.add_menu("system", SYSTEM_USER_LABEL)
    system.add_action(Changes)
