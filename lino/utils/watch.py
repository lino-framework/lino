# Copyright 2012-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""It defines the functions :func:`watch_changes` and
:func:`watch_all_changes`.

Used by :mod:`lino.modlib.changes`

"""
import six
from lino.core import fields

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
    if isinstance(ignore, six.string_types):
        ignore = fields.fields_list(model, ignore)
    if isinstance(master_key, six.string_types):
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
