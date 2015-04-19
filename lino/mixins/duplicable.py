# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the model mixin :class:`Duplicable`.  "duplicable"
[du'plikəblə] means "able to produce a duplicate
['duplikət], ['du:plikeit]".

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino.core import actions
from lino.core import model


class Duplicate(actions.Action):
    """Duplicate the selected row.

    """
    label = _("Duplicate")
    sort_index = 11
    show_in_workflow = False
    readonly = True  # like InsertRow. See docs/blog/2012/0726
    icon_name = 'arrow_divide'

    def is_callable_from(self, caller):
        if isinstance(caller, actions.InsertRow):
            return False
        return True

    def get_action_permission(self, ar, obj, state):
        if ar.get_user().profile.readonly:
            return False
        return super(Duplicate, self).get_action_permission(ar, obj, state)

    def run_from_code(self, ar, **known_values):
        obj = ar.selected_rows[0]
        related = []
        for m, fk in obj._lino_ddh.fklist:
            if fk.name in m.allow_cascaded_delete:
                related.append((fk, m.objects.filter(**{fk.name: obj})))

        if True:
            for f in obj._meta.fields:
                if not f.primary_key:
                    known_values[f.name] = getattr(obj, f.name)
            new = obj.__class__(**known_values)
            # 20120704 create_instances causes fill_from_person() on a
            # CBSS request.
        else:
            # doesn't seem to want to work
            new = obj
            for f in obj._meta.fields:
                if f.primary_key:
                    # causes Django to consider this an unsaved instance
                    setattr(new, f.name, None)

        new.save(force_insert=True)
        new.on_duplicate(ar, None)

        for fk, qs in related:
            for relobj in qs:
                relobj.pk = None  # causes Django to save a copy
                setattr(relobj, fk.name, new)
                relobj.on_duplicate(ar, new)
                relobj.save(force_insert=True)

        return new

    def run_from_ui(self, ar, **kw):
        """This actually runs the action."""
        obj = ar.selected_rows[0]
        new = self.run_from_code(ar)
        kw = dict()
        # kw.update(refresh=True)
        kw.update(message=_("Duplicated %(old)s to %(new)s.") %
                  dict(old=obj, new=new))
        #~ kw.update(new_status=dict(record_id=new.pk))
        ar.success(**kw)
        if ar.actor.detail_action is None or ar.actor.stay_in_grid:
            ar.set_response(refresh_all=True)
        else:
            ar.goto_instance(new)


class Duplicable(model.Model):

    """Adds a row action "Duplicate" which duplicates (creates a clone
    of) the object it was called on.
    
    Subclasses may override :meth:`dd.Model.on_duplicate` to customize the
    default behaviour, which is to copy all fields except the primary
    key and all related objects that are duplicable.

    """
    class Meta:
        abstract = True

    duplicate = Duplicate()
